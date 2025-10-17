import os

# ======== Fix agar tidak error libGL.so.1 (di Streamlit Cloud) ========
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["DISPLAY"] = ":0"
# =====================================================================

import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2

# ==========================
# Load Models
# ==========================
@st.cache_resource
def load_models():
    try:
        # Load YOLO model (deteksi objek)
        yolo_model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")
    except Exception as e:
        st.error(f"Gagal memuat model YOLO: {e}")
        yolo_model = None

    try:
        # Load model Keras (klasifikasi gambar)
        classifier = tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")
    except Exception as e:
        st.error(f"Gagal memuat model Keras: {e}")
        classifier = None

    return yolo_model, classifier

yolo_model, classifier = load_models()

# ==========================
# UI
# ==========================
st.title("🧠 Image Classification & Object Detection App")

menu = st.sidebar.selectbox(
    "Pilih Mode:",
    ["Deteksi Objek (YOLO)", "Klasifikasi Gambar"]
)

uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Gambar yang Diupload", use_container_width=True)

    if menu == "Deteksi Objek (YOLO)":
        if yolo_model is not None:
            try:
                results = yolo_model(img)
                result_img = results[0].plot()  # hasil deteksi (gambar dengan box)
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat deteksi objek: {e}")
        else:
            st.warning("Model YOLO belum dimuat.")

    elif menu == "Klasifikasi Gambar":
        if classifier is not None:
            try:
                # Preprocessing
                img_resized = img.resize((224, 224))
                img_array = image.img_to_array(img_resized)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                # Prediksi
                prediction = classifier.predict(img_array)
                class_index = int(np.argmax(prediction))
                confidence = float(np.max(prediction))

                st.write(f"### Hasil Prediksi: {class_index}")
                st.write(f"Probabilitas: {confidence:.4f}")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat klasifikasi: {e}")
        else:
            st.warning("Model Keras belum dimuat.")
