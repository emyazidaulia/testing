import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Gunakan direktori sementara agar tidak crash
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

# Import YOLO dengan aman
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
    st.warning(f"⚠️ YOLO tidak aktif di environment ini: {e}")
    YOLO_AVAILABLE = False


@st.cache_resource
def load_yolo_model():
    if YOLO_AVAILABLE:
        model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")
        model.overrides["save"] = False  # nonaktifkan penyimpanan otomatis
        model.overrides["project"] = "/tmp"
        return model
    return None


@st.cache_resource
def load_classifier_model():
    return tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")


# ==========================
# UI
# ==========================
st.title("🧠 Image Classification & Object Detection App")

menu = st.sidebar.selectbox("Pilih Mode:", ["Deteksi Objek (YOLO)", "Klasifikasi Gambar"])
uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 Gambar yang Diupload", use_container_width=True)

    if menu == "Deteksi Objek (YOLO)":
        yolo_model = load_yolo_model()
        if yolo_model:
            with st.spinner("🔍 Sedang mendeteksi objek..."):
                results = yolo_model.predict(img, verbose=False)
                result_img = results[0].plot()
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
        else:
            st.error("Model YOLO tidak dapat digunakan di server ini.")

    elif menu == "Klasifikasi Gambar":
        classifier = load_classifier_model()
        with st.spinner("🧩 Sedang melakukan klasifikasi..."):
            img_resized = img.resize((128, 128))
            img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            prediction = classifier.predict(img_array)
            class_index = np.argmax(prediction)
            probability = np.max(prediction)

            st.success("✅ Klasifikasi Berhasil!")
            st.write("### Hasil Prediksi:", class_index)
            st.write("### Probabilitas:", f"{probability:.4f}")
else:
    st.info("📁 Silakan unggah gambar terlebih dahulu.")
