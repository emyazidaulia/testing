import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Setup environment
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

if "page" not in st.session_state:
    st.session_state.page = "home"

# Hilangkan padding bawaan dan sembunyikan header/footer
st.markdown("""
    <style>
    .block-container {padding: 0; margin: 0;}
    header, footer {visibility: hidden;}
    .stApp {overflow: hidden;}
    </style>
""", unsafe_allow_html=True)

# ============================
# HOME PAGE (TAMPILAN PENUH)
# ============================
if st.session_state.page == "home":
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            height: 100%;
            margin: 0;
        }
        .full-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            height: 100vh;
            width: 100vw;
            margin: 0;
            overflow: hidden;
        }
        .side {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2.2rem;
            font-weight: 700;
            color: white;
            text-align: center;
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
        }
        .side:hover {
            transform: scale(1.03);
            filter: brightness(1.05);
        }
        .red {
            background: linear-gradient(135deg, #ff2b2b, #ff6b6b);
        }
        .blue {
            background: linear-gradient(135deg, #007bff, #00bfff);
        }
        .side form {
            position: absolute;
            inset: 0;
        }
        .side button {
            position: absolute;
            inset: 0;
            background: transparent;
            border: none;
            cursor: pointer;
            z-index: 10;
        }
        .label {
            z-index: 5;
            line-height: 1.3;
            pointer-events: none;
        }
        </style>

        <div class="full-container">
            <div class="side red">
                <form action="?page=classify" method="get">
                    <button type="submit"></button>
                    <div class="label">🍝 Eat uncooked pasta<br>(Image Classification)</div>
                </form>
            </div>
            <div class="side blue">
                <form action="?page=detect" method="get">
                    <button type="submit"></button>
                    <div class="label">🥤 Drink salted coke<br>(Object Detection)</div>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Tangkap query parameter untuk berpindah halaman
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.page = query_params["page"]
        st.experimental_rerun()

# ============================
# HALAMAN KLASIFIKASI GAMBAR
# ============================
elif st.session_state.page == "classify":
    st.markdown('<div style="padding:2rem 5rem;">', unsafe_allow_html=True)
    st.title("🍝 Image Classification Mode")

    if st.button("⬅️ Kembali ke Menu Awal"):
        st.session_state.page = "home"
        st.experimental_rerun()

    uploaded_file = st.file_uploader("Unggah gambar untuk diklasifikasi", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="📸 Gambar yang diupload", use_column_width=True)
        model = load_classifier_model()
        with st.spinner("🧩 Sedang melakukan klasifikasi..."):
            img_resized = img.resize((128, 128))
            img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0) / 255.0
            prediction = model.predict(img_array)
            class_index = int(np.argmax(prediction))
            prob = float(np.max(prediction))
        st.success("✅ Klasifikasi Berhasil!")
        st.write("### Hasil Prediksi:", class_index)
        st.write("### Probabilitas:", f"{prob:.4f}")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================
# HALAMAN DETEKSI OBJEK
# ============================
elif st.session_state.page == "detect":
    st.markdown('<div style="padding:2rem 5rem;">', unsafe_allow_html=True)
    st.title("🥤 Object Detection Mode (YOLO)")

    if st.button("⬅️ Kembali ke Menu Awal"):
        st.session_state.page = "home"
        st.experimental_rerun()

    if not YOLO_AVAILABLE:
        st.error(f"⚠️ YOLO tidak tersedia di server ini ({YOLO_IMPORT_ERROR})")

    uploaded_file = st.file_uploader("Unggah gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="📸 Gambar yang diupload", use_column_width=True)
        yolo = load_yolo_model()
        if yolo:
            with st.spinner("🔍 Sedang mendeteksi objek..."):
                results = yolo.predict(img, verbose=False)
                result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_column_width=True)
        else:
            st.error("Model YOLO tidak dapat dijalankan di environment ini.")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)
