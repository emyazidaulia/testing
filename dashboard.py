import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ===== KONFIGURASI DASAR =====
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
    YOLO_AVAILABLE = False
    YOLO_IMPORT_ERROR = str(e)

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

st.set_page_config(page_title="Would You Rather AI", layout="wide")

# ===== STATE HALAMAN =====
if "page" not in st.session_state:
    st.session_state.page = "home"

def goto(page):
    st.session_state.page = page
    st.rerun()

# ====== HOME PAGE ======
if st.session_state.page == "home":
    st.markdown("""
        <style>
        .block-container {padding:0; margin:0;}
        header, footer {visibility:hidden;}
        .split-screen {
            display: grid;
            grid-template-columns: 1fr 1fr;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }
        .left, .right {
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            text-align: center;
        }
        .left { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .right { background: linear-gradient(135deg, #007bff, #00bfff); }

        .center-box {
            padding: 40px 60px;
            border-radius: 20px;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            font-weight: 700;
            font-size: 2rem;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            backdrop-filter: blur(5px);
        }
        .center-box:hover {
            transform: scale(1.05);
            background-color: rgba(255,255,255,0.3);
        }
        </style>

        <div class="split-screen">
            <div class="left">
                <div class="center-box" onclick="window.location.href='?page=classify'">
                    🍝 Eat uncooked pasta<br>(Image Classification)
                </div>
            </div>
            <div class="right">
                <div class="center-box" onclick="window.location.href='?page=detect'">
                    🥤 Drink salted coke<br>(Object Detection)
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sinkronisasi URL → session_state
    query_params = st.query_params
    if "page" in query_params:
        if query_params["page"] == "classify":
            goto("classify")
        elif query_params["page"] == "detect":
            goto("detect")

# ====== IMAGE CLASSIFICATION PAGE ======
elif st.session_state.page == "classify":
    st.title("🍝 Image Classification")
    if st.button("⬅️ Kembali ke Home"):
        goto("home")

    uploaded_file = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar diunggah", use_column_width=True)
        model = load_classifier_model()
        img_resized = img.resize((128, 128))
        arr = tf.keras.preprocessing.image.img_to_array(img_resized)
        arr = np.expand_dims(arr, 0) / 255.0
        with st.spinner("Klasifikasi..."):
            pred = model.predict(arr)
            idx = int(np.argmax(pred))
            prob = float(np.max(pred))
        st.success("✅ Hasil Klasifikasi")
        st.write("Kelas:", idx)
        st.write("Probabilitas:", f"{prob:.4f}")

# ====== OBJECT DETECTION PAGE ======
elif st.session_state.page == "detect":
    st.title("🥤 Object Detection")
    if st.button("⬅️ Kembali ke Home"):
        goto("home")

    if not YOLO_AVAILABLE:
        st.error(f"YOLO tidak tersedia: {YOLO_IMPORT_ERROR}")
    uploaded_file = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar diunggah", use_column_width=True)
        yolo = load_yolo_model()
        if yolo:
            with st.spinner("Mendeteksi..."):
                results = yolo.predict(img, verbose=False)
                result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_column_width=True)
        else:
            st.error("Model YOLO tidak dapat dijalankan di environment ini.")
