# Dal Bhat Image Classifier

A PyTorch image-classification application for distinguishing dal bhat from a negative class.

## What it demonstrates

- Transfer learning with ResNet18
- ImageFolder dataset loading
- Data augmentation
- Class balancing with WeightedRandomSampler
- Frozen-backbone fine-tuning
- Validation accuracy reporting
- Confidence thresholding
- Streamlit inference UI

## Run the app

Install the project dependencies:

```bash
python -m pip install -r requirements-food.txt
streamlit run app.py
```

If no saved model exists, the application trains one from the local dataset before serving predictions.

## Dataset layout

```text
datasets/
├── dalbhat/
└── not_dalbhat/
```

The model should not be presented as a general-purpose food classifier. Its performance is limited by the quality, diversity, and size of the local dataset.
