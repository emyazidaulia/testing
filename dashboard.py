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
        model.overrides["save"] = False
        model.overrides["project"] = "/tmp"
        return model
    return None


@st.cache_resource
def load_classifier_model():
    return tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")


# ==========================
# Tampilan Utama
# ==========================
st.set_page_config(page_title="Would You Rather: AI Edition", layout="wide")

if "mode" not in st.session_state:
    st.session_state.mode = None

if st.session_state.mode is None:
    st.markdown(
        """
        <style>
        .choice-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            gap: 2rem;
        }
        .choice {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            font-weight: 700;
            color: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        .choice:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }
        .red { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .blue { background: linear-gradient(135deg, #007bff, #00bfff); }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="choice-container">
            <div class="choice red" onclick="window.location.href='?mode=classify'">
                🍝 Eat uncooked pasta<br>(Image Classification)
            </div>
            <div class="choice blue" onclick="window.location.href='?mode=detect'">
                🥤 Drink salted coke<br>(Object Detection)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    query_params = st.experimental_get_query_params()
    if "mode" in query_params:
        mode = query_params["mode"][0]
        if mode == "classify":
            st.session_state.mode = "Klasifikasi Gambar"
        elif mode == "detect":
            st.session_state.mode = "Deteksi Objek (YOLO)"
    st.stop()

# ==========================
# Mode Klasifikasi atau Deteksi
# ==========================
st.title(f"🧠 {st.session_state.mode}")

uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 Gambar yang Diupload", use_container_width=True)

    if st.session_state.mode == "Deteksi Objek (YOLO)":
        yolo_model = load_yolo_model()
        if yolo_model:
            with st.spinner("🔍 Sedang mendeteksi objek..."):
                results = yolo_model.predict(img, verbose=False)
                result_img = results[0].plot()
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
        else:
            st.error("Model YOLO tidak dapat digunakan di server ini.")

    elif st.session_state.mode == "Klasifikasi Gambar":
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
