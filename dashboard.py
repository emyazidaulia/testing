import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ========== CONFIG ==========
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

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


# ========== UI ==========
st.set_page_config(page_title="Would You Rather AI", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ======== HALAMAN UTAMA ========
if st.session_state.page == "home":
    st.markdown(
        """
        <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 3rem;
            height: 90vh;
        }
        .box {
            flex: 1;
            height: 70vh;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 25px;
            font-size: 2rem;
            font-weight: 700;
            color: white;
            text-align: center;
            transition: all 0.3s ease;
        }
        .red { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .blue { background: linear-gradient(135deg, #007bff, #00bfff); }
        .box:hover {
            transform: scale(1.03);
            box-shadow: 0 0 25px rgba(0,0,0,0.2);
        }
        button {
            border: none;
            background: none;
            padding: 0;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Tombol besar merah
        if st.button("🍝 Eat uncooked pasta\n(Image Classification)", use
