import torch.nn.functional as F
from torch import nn, optim
import pytorch_lightning as pl
import model_backbones
import loss_functions
from metric import N5K_Metric

CLASS_NAMES = ['Mass']

class RGB_D_Constructor(pl.LightningModule):
    def __init__(self, args,
                 RgbBackbone="SB",
                 DepthBackbon="SB",
                 Decoder="UnetWith4Addattnv4C2MA"):
        super().__init__()
        self.args = args
        # Important : This property activates manual optimization
        self.automatic_optimization = False
        
        self.best_loss = 1000000.0
        loss = getattr(loss_functions, self.args.loss)
        RgbBackbone = getattr(model_backbones, self.args.backbone[0])
        DepthBackbone = getattr(model_backbones, self.args.backbone[1])
        Decoder = getattr(model_backbones, self.args.decoder)

        # Creating an instance of the dynamically declared class
        self.loss_fn = loss()
        self.rgb_backbone = RgbBackbone()
        self.depth_backbone = DepthBackbone()
        self.decoder_net = Decoder(
            self.rgb_backbone.feature_info, self.depth_backbone.feature_info)

    def forward(self, x, d):
        x = self.rgb_backbone(x)
        d = self.depth_backbone(d)
        return self.decoder_net(x, d)

    def extract_batch(self, batch):
        self.images = batch[0]
        self.depth_img = batch[1]
        self.labels = batch[2]

    def test_step(self, batch, batch_idx):
        self.extract_batch(batch)
        self.outputs = self.forward(self.images, self.depth_img)

        # Handle the case where self.outputs is a tuple
        if isinstance(self.outputs, tuple):
            self.outputs = self.outputs[0]

        loss = self.loss_fn(self.outputs, self.labels)
        self._common_step("Test")
        return {"loss": loss}

    def training_step(self, batch, batch_idx):
        self.extract_batch(batch)
        self.opt.zero_grad(set_to_none=True)

        self.outputs = self.forward(self.images, self.depth_img)

        if isinstance(self.outputs, tuple):
            self.outputs = self.outputs[0]

        loss = self.loss_fn(self.outputs, self.labels)
        self.manual_backward(loss)
        self.opt.step()
        self._common_step("Train")
        self.log("Train loss", loss, on_step=False, on_epoch=True)
        return {"loss": loss}

    def _common_step(self, phase):
        # If self.outputs is a tuple, extract the first element
        if isinstance(self.outputs, tuple):
            outputs = self.outputs[0]
        else:
            outputs = self.outputs

        for i in range(len(self.labels)):
            self.Pred_step['Mass'].append(float(outputs[i]))
            self.GT_step['Mass'].append(float(self.labels[i]))

    def on_train_epoch_start(self) -> None:
        self.Pred_step = {class_name: [] for class_name in CLASS_NAMES}
        self.GT_step = {class_name: [] for class_name in CLASS_NAMES}

    def on_test_epoch_start(self) -> None:
        self.Pred_step = {class_name: [] for class_name in CLASS_NAMES}
        self.GT_step = {class_name: [] for class_name in CLASS_NAMES}

    def _common_end(self, phase):
        """_summary_
        reference: https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#train-epoch-level-operations
        """
        return N5K_Metric(phase=phase, groundtruth_values=self.GT_step, prediction_data=self.Pred_step)

    def on_train_epoch_end(self) -> None:
        log_stats = self._common_end("Train")
        log_stats[f"Train last learning rate"] = self.lr_schedulers().get_last_lr()[0]
        self.log_dict(log_stats,
                      on_step=False,
                      on_epoch=True,
                      prog_bar=True,
                      sync_dist=True
                      )
        self.sch['scheduler'].step()

        epoch_loss = self.trainer.logged_metrics["Train loss"]
        print(f'self.best_loss:{self.best_loss}')
        print(f'epoch_loss:{epoch_loss}')
        if epoch_loss < self.best_loss:
            print(f'save model at epoch:{self.current_epoch}')
            self.best_loss = epoch_loss
            self.trainer.save_checkpoint(
                f"{self.args.save_dir}/{self.logger.experiment.name}.ckpt")
            # self.trainer.save_checkpoint(f"model.ckpt")

    def on_test_epoch_end(self) -> None:
        log_stats = self._common_end("Test")
        self.log_dict(log_stats)

    def configure_optimizers(self):
        self.opt = optim.Adam(self.parameters(),
                              lr=self.args.learning_rate,
                              weight_decay=self.args.weight_decay,
                              eps=self.args.epsilon
                              )

        self.sch = {'scheduler': optim.lr_scheduler.ExponentialLR(self.opt, gamma=self.args.decay_rate),
                    'interval': 'epoch',
                    'frequency': 1}
        return {'optimizer': self.opt, 'lr_scheduler': self.sch}