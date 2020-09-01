import torch
from PIL import Image
import matplotlib.pyplot as plt
# from utils import *
import torchvision.transforms as transforms
from models.model import Encoder


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


def load_model(model_path=None):
    """
    Loading model
    """
    model = Encoder()
    if model_path == None:
        model_path = "./best_model.th"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #model = model.load_state_dict(torch.load(model_path, map_location=device))
    #model_dec = torch.load(model_path + "final_dec.pth", map_location=device)
    model.eval()
    return model


def load_labels(vocab_path=None):
    import json
    with open('classes.json', 'r') as file:
        labels = json.load(file)
    return labels


def get_caption_prediction(img_path):

    transform = set_transform()

    labels = load_labels()
    model = load_model()
    # prediction
    with torch.no_grad():
        imgs = Image.open(img_path).convert("RGB")
        img = transform(imgs)
        #img = to_variable(img)
        img = img.unsqueeze(0)
        out = model(img)
        _, preds = torch.max(out.data, 1)
        preds = preds.cpu().detach().numpy()[0]
    preds = labels[str(preds)]
    return preds
