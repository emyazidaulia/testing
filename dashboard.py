import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Konfigurasi lingkungan
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

# State halaman
if "page" not in st.session_state:
    st.session_state.page = "home"

# Hilangkan margin/padding bawaan
st.markdown("""
    <style>
    .block-container {padding: 0; margin: 0;}
    header, footer {visibility: hidden;}
    .stApp {overflow: hidden;}
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk berpindah halaman tanpa reload
def change_page(new_page):
    st.session_state.page = new_page
    st.experimental_rerun()

# ============================
# HOME PAGE (UI LAYAR PENUH)
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
        .label {
            z-index: 5;
            line-height: 1.3;
            pointer-events: none;
        }
        </style>

        <div class="full-container">
            <div class="side red" onclick="sendMessage('classify')">
                <div class="label">🍝 Eat uncooked pasta<br>(Image Classification)</div>
            </div>
            <div class="side blue" onclick="sendMessage('detect')">
                <div class="label">🥤 Drink salted coke<br>(Object Detection)</div>
            </div>
        </div>

        <script>
        const sendMessage = (page) => {
            window.parent.postMessage({page: page}, "*");
        };
        </script>
    """, unsafe_allow_html=True)

    # Tangkap pesan dari JS (klik kotak)
    clicked_page = st.experimental_get_query_params().get("clicked_page", [None])[0]
    if clicked_page:
        change_page(clicked_page)

    # JS listener agar bisa ubah state tanpa reload
    st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            const page = event.data.page;
            if (page) {
                const url = new URL(window.location);
                url.searchParams.set("clicked_page", page);
                window.location.href = url;
            }
        });
        </script>
    """, unsafe_allow_html=True)

# ============================
# KLASIFIKASI GAMBAR
# ============================
elif st.session_state.page == "classify":
    st.markdown('<div style="padding:2rem 5rem;">', unsafe_allow_html=True)
    st.title("🍝 Image Classification Mode")

    if st.button("⬅️ Kembali ke Menu Awal"):
        change_page("home")

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
# DETEKSI OBJEK
# ============================
elif st.session_state.page == "detect":
    st.markdown('<div style="padding:2rem 5rem;">', unsafe_allow_html=True)
    st.title("🥤 Object Detection Mode (YOLO)")

    if st.button("⬅️ Kembali ke Menu Awal"):
        change_page("home")

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
