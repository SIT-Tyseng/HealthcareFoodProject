import numpy as np
from torch import nn
from torch import cat
from torchvision import models
from torchvision.ops.misc import Permute
from model_components import *

class SB(models.SwinTransformer):
    def __init__(self):
        weights = models.swin_b(weights=models.Swin_B_Weights.DEFAULT)
        super().__init__(
            patch_size=[4, 4],
            embed_dim=128,
            depths=[2, 2, 18, 2],
            num_heads=[4, 8, 16, 32],
            window_size=[7, 7],
            stochastic_depth_prob=0.5,
        )
        if weights is not None:
            self.load_state_dict(weights.state_dict(), strict=False)
        self.activations = {}

        index_of_swin_blocks = [1, 3, 5]
        self.features[index_of_swin_blocks[0]].register_forward_hook(self.get_activation(0))
        self.features[index_of_swin_blocks[1]].register_forward_hook(self.get_activation(1))
        self.features[index_of_swin_blocks[2]].register_forward_hook(self.get_activation(2))

        self.feature_info = [1024, 512, 256, 128]

        del self.head

    # Hook
    def get_activation(self, name):
        def hook(model, input, output):
            self.activations[name] = self.permute(output)
        return hook

    def forward(self, x):
        x = self.features(x)
        x = self.permute(x)
        x = [x] # -3 -2 1 0
        for i in np.arange(len(self.activations) - 1, -1, -1): # 3 -2 1 0-
            x.append(self.activations[i])
        return x
    
class DeepSupervision(nn.Module):

    def __init__(self, RGB_info, D_info):
        super().__init__()
        self.flatten = nn.Flatten(1)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

        self.in_feature = [1024, 1024, 512, 256]
        self.mid_feature = [1024, 512, 256, 128]
        self.linear_feature=[512, 256, 128, 64]

        self.decoder_layers = get_UnetDecoder(
            self.mid_feature, self.in_feature, self.linear_feature)
        self.head1, self.head2, self.head3, self.head4, self.head5 = get_heads(
            self.linear_feature)

    def forward(self, x, d):
        out1 = 0.0
        out2 = 0.0
        out3 = 0.0
        out4 = 0.0
        out5 = 0.0
        i = 0
        layer_out = fused_add(d[i], x[i])
        layer_out = self.decoder_layers[i](layer_out)
        x_current = self.flatten(self.avgpool(layer_out))
        out1 += self.head1[i](x_current)
        out2 += self.head2[i](x_current)
        out3 += self.head3[i](x_current)
        out4 += self.head4[i](x_current)
        out5 += self.head5[i](x_current)
        for i in range(1, len(x), 1):
            side = fused_add(d[i], x[i])
            layer_out = cat((layer_out, side), dim=1)
            layer_out = self.decoder_layers[i](layer_out)
            x_current = self.flatten(self.avgpool(layer_out))
            out1 += self.head1[i](x_current)
            out2 += self.head2[i](x_current)
            out3 += self.head3[i](x_current)
            out4 += self.head4[i](x_current)
            out5 += self.head5[i](x_current)
        return out1, out2, out3, out4, out5