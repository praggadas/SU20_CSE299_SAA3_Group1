import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim

class Encoder(nn.Module):
    def __init__(self, en_img_size=14, no_classes=108, extracted_feature=512, size_fc=1000):
        super(Encoder, self).__init__()
    
        # feature extraction model (ResNet18=True)
        resnet = models.resnet18(pretrained=True)
        self._resnet_extractor = nn.Sequential(*(list(resnet.children())[:-2]))
        self.en_img_size = en_img_size
        self.adaptive_pool = nn.AdaptiveAvgPool2d((en_img_size, en_img_size))#14,14,512
        self.fc1 = nn.Linear(en_img_size*en_img_size*extracted_feature, size_fc)
        self.fc2 = nn.Linear(size_fc, no_classes+1)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        if torch.cuda.is_available():
             x = x.cuda()
        feature = self._resnet_extractor(x)
        feature = self.adaptive_pool(feature)
        
        feature =  feature.view(feature.size()[0], -1)
        x = F.relu(self.fc1(feature))
        #x = F.dropout(x,self.dropout)
        x = F.relu(self.fc2(x))
        x = self.softmax(x)
        
        return x

        
        
