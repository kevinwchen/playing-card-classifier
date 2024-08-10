import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from pathlib import Path
import timm
import io
import os

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_PATH = os.path.join(BASE_DIR, f"pytorch_playing_cards_model-{__version__}.pth")

labels = {
    0: "ace of clubs",
    1: "ace of diamonds",
    2: "ace of hearts",
    3: "ace of spades",
    4: "eight of clubs",
    5: "eight of diamonds",
    6: "eight of hearts",
    7: "eight of spades",
    8: "five of clubs",
    9: "five of diamonds",
    10: "five of hearts",
    11: "five of spades",
    12: "four of clubs",
    13: "four of diamonds",
    14: "four of hearts",
    15: "four of spades",
    16: "jack of clubs",
    17: "jack of diamonds",
    18: "jack of hearts",
    19: "jack of spades",
    20: "joker",
    21: "king of clubs",
    22: "king of diamonds",
    23: "king of hearts",
    24: "king of spades",
    25: "nine of clubs",
    26: "nine of diamonds",
    27: "nine of hearts",
    28: "nine of spades",
    29: "queen of clubs",
    30: "queen of diamonds",
    31: "queen of hearts",
    32: "queen of spades",
    33: "seven of clubs",
    34: "seven of diamonds",
    35: "seven of hearts",
    36: "seven of spades",
    37: "six of clubs",
    38: "six of diamonds",
    39: "six of hearts",
    40: "six of spades",
    41: "ten of clubs",
    42: "ten of diamonds",
    43: "ten of hearts",
    44: "ten of spades",
    45: "three of clubs",
    46: "three of diamonds",
    47: "three of hearts",
    48: "three of spades",
    49: "two of clubs",
    50: "two of diamonds",
    51: "two of hearts",
    52: "two of spades",
}


# Define model
class SimpleCardClassifier(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCardClassifier, self).__init__()
        self.base_model = timm.create_model(pretrained_model, pretrained=True)
        model_out_size = self.base_model.num_features

        # Remove the last layer of the pretrained model
        self.features = nn.Sequential(*list(self.base_model.children())[:-1])
        # Make a classifier layer
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(model_out_size, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)


# Hyperparameters
input_size = 128
num_epochs = 5
batch_size = 32
num_classes = 53
pretrained_model = "efficientnet_b0"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleCardClassifier(num_classes=num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()


# Transform from image to tensor
def transform_image(image_bytes):
    transform = transforms.Compose(
        [
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
        ]
    )

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    return transform(image)


# Prediction
def get_prediction(image_bytes):
    image_tensor = transform_image(image_bytes).unsqueeze(0)
    output = model(image_tensor)
    pred = torch.argmax(output, dim=1)
    return labels[pred.item()]
