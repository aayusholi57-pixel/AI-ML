from pathlib import Path

import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms
from torchvision.models import ResNet18_Weights, resnet18


PROJECT_PATH = Path(__file__).resolve().parent
DATASET_ROOT = PROJECT_PATH / "datasets"
MODEL_PATH = PROJECT_PATH / "dalbhat_model_v4.pth"
MODEL_VERSION = 4
IMAGE_SIZE = 224
CLASS_NAMES = ["dalbhat", "not_dalbhat"]
MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(12),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])
validation_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])


class DalbhatClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
        feature_count = backbone.fc.in_features
        backbone.fc = nn.Identity()
        self.backbone = backbone
        self.classifier = nn.Sequential(
            nn.Dropout(0.35),
            nn.Linear(feature_count, 2),
        )

    def forward(self, inputs):
        return self.classifier(self.backbone(inputs))


def load_training_data(transform):
    if not DATASET_ROOT.is_dir():
        raise FileNotFoundError(f"Dataset folder was not found: {DATASET_ROOT}")

    dataset = datasets.ImageFolder(DATASET_ROOT, transform=transform)
    if len(dataset) == 0:
        raise RuntimeError(f"No images were found under {DATASET_ROOT}")
    if dataset.classes != CLASS_NAMES:
        raise RuntimeError(
            f"Expected folders {CLASS_NAMES}, but found {dataset.classes}"
        )
    return dataset


def train_model(epochs=20):
    full_dataset = load_training_data(validation_transform)
    train_dataset = load_training_data(train_transform)
    generator = torch.Generator().manual_seed(42)
    indices = torch.randperm(len(full_dataset), generator=generator).tolist()
    validation_count = max(2, int(len(indices) * 0.2))
    validation_indices = indices[:validation_count]
    train_indices = indices[validation_count:]
    train_data = torch.utils.data.Subset(train_dataset, train_indices)
    validation_data = torch.utils.data.Subset(full_dataset, validation_indices)
    labels = [full_dataset.targets[index] for index in train_indices]
    counts = torch.bincount(torch.tensor(labels), minlength=2).float()
    sample_weights = [1.0 / counts[label] for label in labels]
    sampler = WeightedRandomSampler(sample_weights, len(sample_weights), replacement=True)
    train_loader = DataLoader(train_data, batch_size=8, sampler=sampler)
    validation_loader = DataLoader(validation_data, batch_size=8)
    model = DalbhatClassifier()
    for parameter in model.backbone.parameters():
        parameter.requires_grad = False
    for parameter in model.backbone.layer4.parameters():
        parameter.requires_grad = True
    loss_function = nn.CrossEntropyLoss(weight=1.0 / counts.clamp_min(1))
    optimizer = torch.optim.Adam(
        [
            {"params": model.backbone.layer4.parameters(), "lr": 0.0001},
            {"params": model.classifier.parameters(), "lr": 0.001},
        ]
    )

    for _ in range(epochs):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad()
            loss = loss_function(model(images), labels)
            loss.backward()
            optimizer.step()

    model.eval()
    correct = 0
    with torch.no_grad():
        for images, labels in validation_loader:
            correct += (model(images).argmax(1) == labels).sum().item()

    accuracy = correct / len(validation_data)
    torch.save({"version": MODEL_VERSION, "model_state": model.state_dict()}, MODEL_PATH)
    return model, accuracy


def load_model():
    model = DalbhatClassifier()
    checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    if checkpoint.get("version") != MODEL_VERSION:
        raise RuntimeError("This model was trained with an older model version")
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model


def load_scene_model():
    weights = ResNet18_Weights.DEFAULT
    model = resnet18(weights=weights)
    model.eval()
    return model, weights.meta["categories"]


NON_FOOD_LABELS = (
    "person", "man", "woman", "boy", "girl", "football", "soccer",
    "jersey", "stadium", "ball", "player", "basketball", "tennis",
    "dog", "cat", "horse", "bird", "car", "truck", "motorcycle",
)


def predict(model, image, scene_model=None, scene_categories=None):
    image = image.convert("RGB")
    if scene_model is not None and scene_categories is not None:
        scene_input = validation_transform(image).unsqueeze(0)
        with torch.no_grad():
            scene_probabilities = torch.softmax(scene_model(scene_input), dim=1)[0]
        top_indices = scene_probabilities.topk(5).indices.tolist()
        scene_labels = [scene_categories[index].lower() for index in top_indices]
        scene_confidence = max(float(scene_probabilities[index]) for index in top_indices)
        if scene_confidence >= 0.20 and any(
            keyword in label for label in scene_labels for keyword in NON_FOOD_LABELS
        ):
            return "not_dalbhat", scene_confidence

    image_tensor = validation_transform(image).unsqueeze(0)
    with torch.no_grad():
        probabilities = torch.softmax(model(image_tensor), dim=1)[0]
    class_index = int(probabilities.argmax())
    confidence = float(probabilities[class_index])
    if confidence < 0.80:
        return "uncertain", confidence
    return CLASS_NAMES[class_index], confidence


if __name__ == "__main__":
    trained_model, validation_accuracy = train_model()
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Validation accuracy: {validation_accuracy:.1%}")