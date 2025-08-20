import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import itertools
from PIL import Image
from torchvision import models
from torch.autograd import Variable
# from thop import profile
# # from spikingjelly.activation_based.neuron import (
# #     LIFNode, IFNode, ParametricLIFNode,
# # )
# # from spikingjelly.activation_based import neuron, functional, layer, surrogate
# from einops import rearrange, repeat
# from timm.models.layers import DropPath

v_th = 0.15

alpha = 1 / (2 ** 0.5)

decay = 0.25  # 0.25 # decay constants

# class Spiking_Residual_Block(nn.Module):
#     def __init__(self, dim):
#         super(Spiking_Residual_Block, self).__init__()
#         functional.set_step_mode(self, step_mode='m')
#         self.residual = nn.Sequential(
#             LIFNode(v_threshold=v_th, backend='cupy', step_mode='m', decay_input=False),
#             layer.Conv2d(dim, dim, kernel_size=3, stride=1, padding=1, bias=False, step_mode='m'),
#             layer.ThresholdDependentBatchNorm3d(num_features=dim, alpha=alpha, v_th=v_th, affine=True),
#
#             LIFNode(v_threshold=v_th, backend='cupy', step_mode='m', decay_input=False),
#             layer.Conv2d(dim, dim, kernel_size=3, stride=1, padding=1, bias=False,
#                          step_mode='m'),
#             layer.ThresholdDependentBatchNorm3d(num_features=dim, alpha=alpha, v_th=v_th * 0.2, affine=True),
#         )
#         self.shortcut = nn.Sequential(
#             layer.Conv2d(dim, dim, kernel_size=3, stride=1, padding=1,
#                          bias=False, step_mode='m'),
#             layer.ThresholdDependentBatchNorm3d(num_features=dim, alpha=alpha,
#                                                 v_th=v_th, affine=True),
#         )
#         self.attn = layer.MultiDimensionalAttention(T=4, reduction_t=4, reduction_c=16, kernel_size=3, C=dim)
#
#     def forward(self, x):
#         shortcut = torch.clone(x)
#         out = self.residual(x) + self.shortcut(x)
#         # out = self.attn(out) + shortcut
#         return out
class MultiSpike4(nn.Module):

    class quant4(torch.autograd.Function):

        @staticmethod
        def forward(ctx, input):
            ctx.save_for_backward(input)
            return torch.round(torch.clamp(input, min=0, max=4))

        @staticmethod
        def backward(ctx, grad_output):
            input, = ctx.saved_tensors
            grad_input = grad_output.clone()
            #             print("grad_input:",grad_input)
            grad_input[input < 0] = 0
            grad_input[input > 4] = 0
            return grad_input

    def forward(self, x):
        return self.quant4.apply(x)

def autopad(k, p=None, d=1):  # kernel, padding, dilation
    # Pad to 'same' shape outputs
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p

class mem_update(nn.Module):
    def __init__(self, act=False):
        super(mem_update, self).__init__()
        # self.actFun= torch.nn.LeakyReLU(0.2, inplace=False)

        self.act = act
        self.qtrick = MultiSpike4()  # change the max value

    def forward(self, x):

        spike = torch.zeros_like(x[0]).to(x.device)
        output = torch.zeros_like(x)
        mem_old = 0
        time_window = x.shape[0]
        for i in range(time_window):
            if i >= 1:
                mem = (mem_old - spike.detach()) * decay + x[i]

            else:
                mem = x[i]
            spike = self.qtrick(mem)

            mem_old = mem.clone()
            output[i] = spike
        # print(output[0][0][0][0])
        return output


class SpikeConv(nn.Module):
    # Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)
    default_act = nn.SiLU()  # default activation

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        super().__init__()
        self.conv = nn.Conv2d(c1, c2, k, s, autopad(k, p, d), groups=g, dilation=d, bias=False)
        self.lif = mem_update()
        self.bn = nn.BatchNorm2d(c2)
        self.s = s
        # self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()

    def forward(self, x):
        T, B, C, H, W = x.shape
        H_new = int(H / self.s)
        W_new = int(W / self.s)
        x = self.lif(x)
        x = self.bn(self.conv(x.flatten(0, 1))).reshape(T, B, -1, H_new, W_new)
        return x

class cleaner(nn.Module):
    def __init__(self):
        super(cleaner, self).__init__()
        
        # Initial convolutional layers
        self.conv1 = ConvLayer(3, 32, kernel_size=3, stride=1)
        # self.conv1 = ConvLayer(1, 32, kernel_size=3, stride=1)
        self.conv2 = ConvLayer(32, 32, kernel_size=3, stride=1)

        # DuRBs
        self.block1 = DuRB_p2(k1_size=5, k2_size=3, dilation=1)
        self.block2 = DuRB_p2(k1_size=7, k2_size=5, dilation=1)
        self.block3 = DuRB_p(k1_size=7, k2_size=5, dilation=2)
        self.block4 = DuRB_p(k1_size=11, k2_size=7, dilation=2)
        self.block5 = DuRB_p2(k1_size=11, k2_size=5, dilation=1)
        self.block6 = DuRB_p2(k1_size=11, k2_size=7, dilation=3)

        # Last layers
        self.conv3 = ConvLayer(32, 32, kernel_size=3, stride=1)
        self.conv4 = ConvLayer(32, 3, kernel_size=3, stride=1)
        # self.conv4 = ConvLayer(32, 1, kernel_size=3, stride=1)

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        
    def forward(self, x):        
        out = self.relu(self.conv1(x))
        out = self.relu(self.conv2(out))
        res = out

        # out, res = self.block1(out, res)
        out, res = self.block2(out, res)
        out, res = self.block3(out, res)
        out, res = self.block4(out, res)
        out, res = self.block5(out, res)
        # out, res = self.block6(out, res)

        out = self.relu(self.conv3(out))
        out = self.tanh(self.conv4(out))
        out = out + x

        return out

class cleaner_WO(nn.Module):
    def __init__(self):
        super(cleaner_WO, self).__init__()

        # Initial convolutional layers
        self.conv1 = ConvLayer(3, 32, kernel_size=3, stride=1)
        # self.conv1 = ConvLayer(1, 32, kernel_size=3, stride=1)
        self.conv2 = ConvLayer(32, 32, kernel_size=3, stride=1)

        # DuRBs
        self.block1 = DuRB_p2(k1_size=5, k2_size=3, dilation=1)
        self.block2 = DuRB_p2(k1_size=7, k2_size=5, dilation=1)
        self.block3 = DuRB_p(k1_size=7, k2_size=5, dilation=2)
        self.block4 = DuRB_p(k1_size=11, k2_size=7, dilation=2)
        self.block5 = DuRB_p2(k1_size=11, k2_size=5, dilation=1)
        self.block6 = DuRB_p2(k1_size=11, k2_size=7, dilation=3)

        # Last layers
        self.conv3 = ConvLayer(32, 32, kernel_size=3, stride=1)
        self.conv4 = ConvLayer(32, 3, kernel_size=3, stride=1)
        # self.conv4 = ConvLayer(32, 1, kernel_size=3, stride=1)

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        out = self.relu(self.conv1(x))
        out = self.relu(self.conv2(out))
        res = out

        # out, res = self.block1(out, res)
        out, res = self.block2(out, res)
        out, res = self.block5(out, res)
        # out, res = self.block6(out, res)

        out = self.relu(self.conv3(out))
        out = self.tanh(self.conv4(out))
        out = out + x

        return out

class cleaner_2_block(nn.Module):
    def __init__(self):
        super(cleaner_2_block, self).__init__()

        # Initial convolutional layers
        self.conv1 = ConvLayer(3, 32, kernel_size=3, stride=1)
        # self.conv1 = ConvLayer(1, 32, kernel_size=3, stride=1)
        self.conv2 = ConvLayer(32, 32, kernel_size=3, stride=1)

        # DuRBs
        self.block1 = DuRB_p2(k1_size=5, k2_size=3, dilation=1)
        self.block2 = DuRB_p2(k1_size=7, k2_size=5, dilation=1)
        self.block3 = DuRB_p(k1_size=7, k2_size=5, dilation=2)
        self.block4 = DuRB_p(k1_size=11, k2_size=7, dilation=2)
        self.block5 = DuRB_p2(k1_size=11, k2_size=5, dilation=1)
        self.block6 = DuRB_p2(k1_size=11, k2_size=7, dilation=3)

        # Last layers
        self.conv3 = ConvLayer(32, 32, kernel_size=3, stride=1)
        self.conv4 = ConvLayer(32, 3, kernel_size=3, stride=1)
        # self.conv4 = ConvLayer(32, 1, kernel_size=3, stride=1)

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        out = self.relu(self.conv1(x))
        out = self.relu(self.conv2(out))
        res = out

        # out, res = self.block1(out, res)
        # out, res = self.block2(out, res)
        # out, res = self.block3(out, res)
        out, res = self.block4(out, res)
        out, res = self.block5(out, res)
        # out, res = self.block6(out, res)

        out = self.relu(self.conv3(out))
        out = self.tanh(self.conv4(out))
        out = out + x

        return out


class cleaner_6_block(nn.Module):
    def __init__(self):
        super(cleaner_6_block, self).__init__()

        # Initial convolutional layers
        self.conv1 = ConvLayer(3, 32, kernel_size=3, stride=1)
        # self.conv1 = ConvLayer(1, 32, kernel_size=3, stride=1)
        self.conv2 = ConvLayer(32, 32, kernel_size=3, stride=1)

        # DuRBs
        self.block1 = DuRB_p2(k1_size=5, k2_size=3, dilation=1)
        self.block2 = DuRB_p2(k1_size=7, k2_size=5, dilation=1)
        self.block3 = DuRB_p(k1_size=7, k2_size=5, dilation=2)
        self.block4 = DuRB_p(k1_size=11, k2_size=7, dilation=2)
        self.block7 = DuRB_p(k1_size=11, k2_size=7, dilation=2)
        self.block5 = DuRB_p2(k1_size=11, k2_size=5, dilation=1)
        self.block6 = DuRB_p2(k1_size=11, k2_size=7, dilation=3)
        self.block8 = DuRB_p2(k1_size=11, k2_size=7, dilation=3)

        # Last layers
        self.conv3 = ConvLayer(32, 32, kernel_size=3, stride=1)
        self.conv4 = ConvLayer(32, 3, kernel_size=3, stride=1)
        # self.conv4 = ConvLayer(32, 1, kernel_size=3, stride=1)

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        out = self.relu(self.conv1(x))
        out = self.relu(self.conv2(out))
        res = out

        # out, res = self.block1(out, res)
        out, res = self.block2(out, res)
        out, res = self.block3(out, res)
        out, res = self.block4(out, res)
        out, res = self.block7(out, res)
        out, res = self.block5(out, res)
        out, res = self.block8(out, res)
        # out, res = self.block6(out, res)

        out = self.relu(self.conv3(out))
        out = self.tanh(self.conv4(out))
        out = out + x

        return out

class DuRB_p2(nn.Module):
    def __init__(self, in_dim=32, out_dim=32, res_dim=32, k1_size=3, k2_size=1, dilation=1, norm_type="batch_norm",
                 with_relu=True):
        super(DuRB_p2, self).__init__()

        self.conv1 = ConvLayer(in_dim, in_dim, 3, 1)
        self.norm1 = FeatNorm(norm_type, in_dim)
        self.conv2 = ConvLayer(in_dim, in_dim, 3, 1)
        self.norm2 = FeatNorm(norm_type, in_dim)

        # T^{l}_{1}: (conv.+ bn)
        self.up_conv = ConvLayer(in_dim, res_dim, kernel_size=k1_size, stride=1, dilation=dilation)
        self.up_norm = FeatNorm(norm_type, res_dim)

        # T^{l}_{2}: (conv.+ bn)
        self.down_conv = ConvLayer(res_dim, out_dim, kernel_size=k2_size, stride=1)
        self.down_norm = FeatNorm(norm_type, out_dim)

        self.with_relu = with_relu
        self.relu = nn.ReLU()

    def forward(self, x, res):
        x_r = x

        x = self.relu(self.norm1(self.conv1(x)))
        x = self.conv2(x)
        x += x_r
        x = self.relu(self.norm2(x))

        # T^{l}_{1}
        x = self.up_norm(self.up_conv(x))
        x += res
        x = self.relu(x)
        res = x

        # T^{l}_{2}
        x = self.down_norm(self.down_conv(x))
        x += x_r

        if self.with_relu:
            x = self.relu(x)
        else:
            pass

        return x, res

        
class DuRB_p(nn.Module):     
    def __init__(self, in_dim=32, out_dim=32, res_dim=32, k1_size=3, k2_size=1, dilation=1, norm_type="batch_norm", with_relu=True):
        super(DuRB_p, self).__init__()
        
        self.conv1 = ConvLayer(in_dim, in_dim, 3, 1)
        self.conv2 = ConvLayer(in_dim, in_dim, 3, 1)
        
        # T^{l}_{1}: (conv.)
        self.up_conv = ConvLayer(in_dim, res_dim, kernel_size=k1_size, stride=1, dilation=dilation)

        # self.mamba = MambaBlock(channels=32)
        self.snn = SpikeConv(32,32)

        # T^{l}_{2}: (conv.)
        self.down_conv = ConvLayer(res_dim, out_dim, kernel_size=k2_size, stride=1)

        self.with_relu = with_relu            
        self.relu = nn.ReLU()

    def forward(self, x, res):
        x_r = x
        
        x = self.relu(self.conv1(x))
        x = self.conv2(x)
        x+= x_r
        x = self.relu(x)
        
        # T^{l}_{1}
        x = self.up_conv(x)
        x+= res
        x = self.relu(x)
        res = x

        # T^{l}_{2}
        x = self.down_conv(x)
        # x = self.mamba(x)
        if len(x.shape) < 5:
            x = (x.unsqueeze(0)).repeat(4, 1, 1, 1, 1)
        x = self.snn(x)
        x = x.mean(dim=0)
        x+= x_r

        if self.with_relu:
            x = self.relu(x)
        else:
            pass
            
        return x, res
       

#---------------------------------------------------------        
class ConvLayer(nn.Module):
    def __init__(self, in_dim, out_dim, kernel_size, stride, dilation=1):
        super(ConvLayer, self).__init__()
        reflect_padding = int(dilation * (kernel_size - 1) / 2)
        self.reflection_pad = nn.ReflectionPad2d(reflect_padding)
        self.conv2d = nn.Conv2d(in_dim, out_dim, kernel_size, stride, dilation=dilation)

    def forward(self, x):
        out = self.reflection_pad(x)
        out = self.conv2d(out)        
        return out

        
class FeatNorm(nn.Module):
    def __init__(self, norm_type, dim):
        super(FeatNorm, self).__init__()
        if norm_type == "instance":
            self.norm = InsNorm(dim)
        elif norm_type == "batch_norm":
            self.norm = nn.BatchNorm2d(dim)
        else:
            raise Exception("Normalization type incorrect.")

    def forward(self, x):
        out = self.norm(x)        
        return out
