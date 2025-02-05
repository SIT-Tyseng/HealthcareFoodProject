import torch
from torch import nn
from torch import add, cat, mul


@torch.jit.script
def fused_mul(x, y):
    return mul(x, y)

@torch.jit.script
def fused_add(x, y):
    return add(x, y)



class UnetBlock(nn.Module):
    # reference https://github.com/milesial/Pytorch-UNet/blob/master/unet/unet_parts.py
    def __init__(self, in_feature, mid_feature, out_feature):
        super().__init__()
        self.unet_block = nn.Sequential(
            nn.Conv2d(in_feature, mid_feature,
                      kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_feature, out_feature,
                      kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.unet_block(x)
    

def get_UnetDecoder(mid_feature, in_feature, linear_feature):
    decoder_layers = nn.ModuleList()
    for i in range(0, len(mid_feature), 1):
        decoder_layers.append(
            nn.Sequential(
                nn.ConvTranspose2d(
                in_feature[i], mid_feature[i], kernel_size=2, stride=2),
                UnetBlock(
                    mid_feature[i], linear_feature[i], linear_feature[i]),
            ) 
        )
    return decoder_layers

def get_heads(linear_feature):
    head1 = nn.ModuleList()
    head2 = nn.ModuleList()
    head3 = nn.ModuleList()
    head4 = nn.ModuleList()
    head5 = nn.ModuleList()
    for i in range(0, len(linear_feature), 1):
        head1.append(
            nn.Linear(in_features=linear_feature[i], out_features=1))
        head2.append(
            nn.Linear(in_features=linear_feature[i], out_features=1))
        head3.append(
            nn.Linear(in_features=linear_feature[i], out_features=1))
        head4.append(
            nn.Linear(in_features=linear_feature[i], out_features=1))
        head5.append(
            nn.Linear(in_features=linear_feature[i], out_features=1))
    return head1, head2, head3, head4, head5