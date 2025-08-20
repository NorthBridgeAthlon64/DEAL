import sys
sys.path.insert(1, '../')
import torchvision
import torchvision.transforms as transforms
# from attack_model_6block import *
import warnings
import torch
torch.autograd.set_detect_anomaly(True)
import numpy as np
import torch.nn as nn
import os
from PIL import Image

# 忽略特定警告
warnings.filterwarnings("ignore", \
                        message="Default upsampling behavior when mode=bilinear is changed to align_corners=False")
warnings.filterwarnings("ignore", category=UserWarning)

# from torch.utils.data import DataLoader
# from models import data_convertors
# from models.model_ne import NE as cleaner
from models.snn import cleaner
# from models.utilities import ssim
transform = transforms.Compose([transforms.ToTensor()])

# torch.cuda.set_device(0)
cleaner = cleaner().cuda()
cleaner = nn.DataParallel(cleaner, device_ids=[0])#根据训练时是不是多卡来加

# cleaner.load_state_dict(torch.load('/data2/s503-6/wzj/code/dust/trainres/logs/TestScale_50/dstroot/epoch_839_res_model.pt'))
cleaner.load_state_dict(torch.load('./checkpoint/epoch_839_res_model.pt',map_location='cuda:0'))
cleaner.eval()

# cleaner = cleaner().to('cuda:1')
# cleaner = torch.nn.DataParallel(cleaner, device_ids=[1, 3])
# cleaner.load_state_dict(torch.load('/data2/s503-6/wzj/code/dust/trainres/logs/X4/dstroot/epoch_839_res_model.pt'))

ImageFolder = './Ir_50'
ResultFolder = './test_result'

Images = os.listdir(ImageFolder)
Images = sorted(Images)

if not os.path.exists(ResultFolder):
    os.makedirs(ResultFolder)

with torch.no_grad():
    print('Start Test:')
    for img in Images:
        ImgIndex = img
        print(ImgIndex)

        img = Image.open(os.path.join(ImageFolder, img))
        img = transform(img)
        img = img.unsqueeze(0)
        img = img.cuda()
        # img = img.to('cuda:1')
        img = img.expand(1, 3, -1, -1)

        cleaned = cleaner(img)
        cleaned = cleaned.squeeze(0)

        torchvision.utils.save_image(cleaned, os.path.join(ResultFolder, ImgIndex), nrow=1)