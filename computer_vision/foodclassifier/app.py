"""Streamlit inference UI for the Dal Bhat classifier."""

from pathlib import Path
import sys

import streamlit as st
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from train import MODEL_PATH, load_model, load_scene_model, predict  # noqa: E402


st.set_page_config(page_title="Dal Bhat Classifier", page_icon="🍛")
st.title("Dal Bhat Classifier")
st.write("Upload an image to classify it as dal bhat, not dal bhat, or uncertain.")
st.warning(
    "This model is trained on the local dataset only. Results are limited by "
    "dataset size, diversity, labeling quality, and image conditions."
)


@st.cache_resource
def get_models():
    """Load the trained classifier and optional scene model."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            "Trained model not found. Run python train.py in this folder first."
        )
    model = load_model()
    scene_model, scene_categories = load_scene_model()
    return model, scene_model, scene_categories


try:
    model, scene_model, scene_categories = get_models()
except Exception as error:
    st.error(str(error))
    st.stop()

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", width="stretch")
    label, confidence = predict(model, image, scene_model, scene_categories)

    if label == "dalbhat":
        st.success(f"Prediction: Dal Bhat ({confidence:.1%} confidence)")
    elif label == "uncertain":
        st.info(
            f"Prediction uncertain ({confidence:.1%} confidence). "
            "Use a clearer image or add more training examples."
        )
    else:
        st.warning(f"Prediction: Not Dal Bhat ({confidence:.1%} confidence)")
