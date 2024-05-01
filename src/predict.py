import torch
from torchvision import transforms
from PIL import Image

# Load the embedding model with the last layer removed
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()

# Preprocessing for images
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Embed function that embeds the image and returns the result
def embed_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image_tensor = preprocess(image)
    with torch.no_grad():
        output = model(image_tensor.unsqueeze(0)).squeeze().tolist()
    return {"result": output}