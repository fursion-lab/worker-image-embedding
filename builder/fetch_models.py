import torch
from concurrent.futures import ThreadPoolExecutor


def load_model():
    '''
    Load and cache models in parallel
    '''
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)

    return model


models = {}

models['base'] = load_model()
