import torch
from PIL import Image
import numpy as np
from data_loader import set_transform
import torchvision.transforms as transforms
import pickle


# with open("bn_map.pickle", "rb") as f:
#     bn_map = pickle.load(f)

def set_transform(resize=(256, 256), crop_size=(224, 224), horizontal_flip=False, normalize=True):
    compose_lst = []
    if resize is not None:
        compose_lst.append(transforms.Resize(resize))
    if crop_size is not None:
        compose_lst.append(transforms.RandomCrop(crop_size))
    if horizontal_flip:
        compose_lst.append(transforms.RandomHorizontalFlip())
    compose_lst.append(transforms.ToTensor())
    if normalize:
        compose_lst.append(transforms.Normalize((0.485, 0.456, 0.406),
                                                (0.229, 0.224, 0.225)))

    transform = transforms.Compose(compose_lst)

    return transform


def load_mode_and_predict(image_name):
    model_path = "./model/final_model.th"
    model = torch.load(model_path, map_location="cpu")
    model = model.eval()
    model.use_cuda = False

    img = process_image(image_name)
    img = img.unsqueeze(0)

    out = model(img)

    _, preds = torch.max(out.data, 1)
    preds = preds.cpu().detach().numpy()

    preds = bn_map[preds[0]]

    return preds


def process_image(image_name):
    """
       Takes an image name and converted into Matrix (RGB)
    """
    transform = set_transform()
    image = Image.open(image_name).convert('RGB')
    image = transform(image)

    return image
