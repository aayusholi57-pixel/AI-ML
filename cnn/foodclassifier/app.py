from pathlib import Path
import sys

import streamlit as st
from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import (  # noqa: E402
    MODEL_PATH,
    load_model,
    load_scene_model,
    predict,
    train_model,
)


st.set_page_config(page_title="Dal Bhat Classifier", page_icon="🍛")
st.title("Dal Bhat Classifier")
st.write("Upload a food image to check whether it is dal bhat.")
st.warning(
    "This model is trained only on the images in the datasets folder. "
    "Add more varied non-dal-bhat and human/background images for reliable rejection."
)


@st.cache_resource
def get_model():
    scene_model, scene_categories = load_scene_model()
    if MODEL_PATH.exists():
        return load_model(), scene_model, scene_categories, None
    model, accuracy = train_model(epochs=30)
    return model, scene_model, scene_categories, accuracy


try:
    model, scene_model, scene_categories, validation_accuracy = get_model()
except Exception as error:
    st.error(str(error))
    st.stop()

if validation_accuracy is not None:
    st.info(f"Model trained successfully. Validation accuracy: {validation_accuracy:.1%}")

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
            "Use a clearer food image or add more training images."
        )
    else:
        st.warning(f"Prediction: Not Dal Bhat ({confidence:.1%} confidence)")