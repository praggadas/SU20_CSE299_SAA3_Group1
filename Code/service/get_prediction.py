import torch
from PIL import Image
import numpy as np
from data_loader import set_transform

import pickle
with open("bn_map.pickle","rb") as f:
    bn_map=pickle.load(f)
    


def load_mode_and_predict(image_name):
	"""
	Loading model and prediction
	"""
    model_path = "./model/final_model.th"
    model = torch.load(model_path,map_location="cpu")
    model = model.eval()
    model.use_cuda=False
    
    img = process_image(image_name)
    img = img.unsqueeze(0)
    
    out=model(img)
    
    _, preds = torch.max(out.data, 1)
    preds    =  preds.cpu().detach().numpy()
    
    preds=bn_map[preds[0]]
    
    return preds
        
def process_image(image_name):
    """
       Takes an image name and converted into Matrix (RGB)
    """
    transform = set_transform()
    image = Image.open(image_name).convert('RGB')
    image = transform(image)
    
    return image
