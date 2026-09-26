# Dal Bhat Image Classifier

A focused PyTorch computer-vision application for distinguishing **dal bhat** from a negative class, with a Streamlit inference interface.

## Engineering highlights

- ResNet18 transfer learning
- ImageFolder dataset loading
- Data augmentation
- Class balancing with WeightedRandomSampler
- Frozen-backbone fine-tuning with a trainable final block
- Deterministic train/validation split
- Versioned model checkpoints
- CPU-safe checkpoint loading
- Confidence thresholding and an optional scene-sanity check
- Streamlit inference UI
- Automated execution tests in GitHub Actions

## Architecture

    dataset/
       ↓
    ImageFolder + augmentation
       ↓
    ResNet18 transfer learning
       ↓
    validation + checkpoint
       ↓
    Streamlit upload
       ↓
    prediction / uncertain result

## Run training

Install dependencies:

    python -m pip install -r requirements-food.txt

Train the model explicitly:

    python train.py

The generated checkpoint is ignored by Git and is intentionally not required in the source repository.

## Run the app

After training:

    streamlit run app.py

The application reports a clear error if the checkpoint has not been generated.

## Dataset layout

    datasets/
    ├── dalbhat/
    └── not_dalbhat/

## Limitations

This is an educational binary classifier, not a general-purpose food-recognition model. Performance depends on dataset size, class balance, image diversity, labeling quality, and real-world lighting/background conditions.

The repository does not claim production-level accuracy without a representative benchmark dataset.
