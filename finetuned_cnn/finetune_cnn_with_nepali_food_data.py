import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os




class SimpleResNetWithConv(nn.Module):
    def __init__(self, num_classes=9):
        super().__init__()
       
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        
       
        for param in resnet.parameters():
            param.requires_grad = False
        self.backbone = nn.Sequential(*list(resnet.children())[:-2]) 
        self.conv = nn.Conv2d(in_channels=2048, out_channels=1000, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=1000, out_channels=512, kernel_size=3, padding=1)
        self.my_relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)
        self.my_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.linear_1 = nn.Linear(512, 125)
        self.linear_2 = nn.Linear(125, num_classes)
    
    def forward(self, x):
       
        x = self.backbone(x)
        
        x = self.my_relu(self.conv(x))
        x = self.my_relu(self.conv2(x))
        x = self.my_pool(x)
        x = torch.flatten(x, 1)
        x = self.linear_1(x)
        x = self.dropout(x)
        return self.linear_2(x)



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")




train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


base_dataset_path = "/home/ubuntu/.cache/kagglehub/datasets/saurabkunwar/nepali-food-images/versions/1/dataset"
train_dir = os.path.join(base_dataset_path, "train")

train_dataset = datasets.ImageFolder(root=train_dir, transform=train_transforms)


train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


num_classes = len(train_dataset.classes)
print(f"Found {num_classes} classes: {train_dataset.classes}")


def train_model():
    
    model =  SimpleResNetWithConv(num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    
    # Hand ONLY the added layers to the optimizer (backbone remains untouched)[cite: 1]
    trainable_params = [
        *model.conv .parameters(),
        *model.conv2.parameters(),
        *model.linear_1.parameters(),
        *model.linear_2.parameters()
    ]
    optimizer = optim.Adam(trainable_params, lr=1e-3)
    
    # ----------------------------------------------------
    # 4. Training Loop
    # ----------------------------------------------------
    model.train()  
    epochs = 200    
    
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
    
            optimizer.zero_grad()               # 1. Clear old gradients[cite: 1, 2, 5]
            outputs = model(images)             # 2. Forward pass guess[cite: 1, 2, 4]
            loss = criterion(outputs, labels)   # 3. Grade the guess[cite: 1, 2]
            loss.backward()                     # 4. Assign blame[cite: 1, 2, 5]
            optimizer.step()                    # 5. Turn dials on custom layers[cite: 1, 2, 5]
    
            total_loss += loss.item()
            
    
        print(f"Epoch {epoch} | Loss: {total_loss / 50:.4f}")
    
    
    
    # ----------------------------------------------------
    # 5. Save the Weights Locally
    # ----------------------------------------------------
    torch.save(model.state_dict(), "custom_resnet_cifar10.pth")
    
    print("Model weights successfully saved to custom_resnet_cifar10.pth")