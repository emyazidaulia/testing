import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# KONFIGURASI GLOBAL
# ==========================
st.set_page_config(page_title="Dashboard Deteksi & Klasifikasi", layout="wide")

CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']

# ==========================
# LOAD MODEL
# ==========================
@st.cache_resource
def load_models():
    try:
        yolo_model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")
        classifier = tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")
        return yolo_model, classifier, None
    except Exception as e:
        return None, None, str(e)

yolo_model, classifier, load_err = load_models()

# ==========================
# NAVIGASI HALAMAN
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# Sidebar Navigasi
with st.sidebar:
    st.title("📊 Navigasi")
    st.button("🏠 Home", on_click=lambda: go_to("home"))
    st.button("🧩 Deteksi Objek", on_click=lambda: go_to("deteksi"))
    st.button("🖼️ Klasifikasi Gambar", on_click=lambda: go_to("klasifikasi"))

# ==========================
# HALAMAN HOME (dengan background animasi)
# ==========================
if st.session_state.page == "home":
    background_images = [
        "sample_images/bg1.jpg",
        "sample_images/bg2.jpg",
        "sample_images/bg3.jpg"
    ]

    st.markdown(f"""
        <style>
        @keyframes changeBackground {{
            0%   {{ background-image: url('{background_images[0]}'); }}
            33%  {{ background-image: url('{background_images[1]}'); }}
            66%  {{ background-image: url('{background_images[2]}'); }}
            100% {{ background-image: url('{background_images[0]}'); }}
        }}
        .stApp {{
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            animation: changeBackground 18s infinite ease-in-out;
            transition: background-image 2s ease-in-out;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="text-align:center; color:white; text-shadow: 2px 2px 8px black;">
            🌍 Dashboard Deteksi & Klasifikasi Citra
        </h1>
        <p style="text-align:center; color:white; font-size:18px;">
            Jelajahi kemampuan model deteksi objek YOLO dan klasifikasi gambar dengan CNN.  
            Klik menu di sidebar untuk memulai 🔍
        </p>
    """, unsafe_allow_html=True)

# ==========================
# HALAMAN DETEKSI OBJEK
# ==========================
elif st.session_state.page == "deteksi":
    st.markdown(
        "<style>.stApp {background-color: #f7f7f7 !important;}</style>",
        unsafe_allow_html=True
    )

    st.title("🧩 Deteksi Objek")
    st.write("Unggah gambar untuk mendeteksi objek menggunakan model YOLO.")

    uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Gambar yang diunggah", use_container_width=True)

        if yolo_model:
            results = yolo_model(img)
            result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
        else:
            st.error("Model YOLO belum berhasil dimuat.")

# ==========================
# HALAMAN KLASIFIKASI GAMBAR
# ==========================
elif st.session_state.page == "klasifikasi":
    st.markdown(
        "<style>.stApp {background-color: #ffffff !important;}</style>",
        unsafe_allow_html=True
    )

    st.title("🖼️ Klasifikasi Gambar")
    st.write("Unggah gambar untuk diklasifikasikan menggunakan model CNN.")

    uploaded_file = st.file_uploader("Pilih gambar untuk diklasifikasikan...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar yang diunggah", use_container_width=True)

        if classifier:
            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            predictions = classifier.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            st.success(
                f"Hasil Prediksi: **{CLASS_NAMES[np.argmax(score)]}** "
                f"({100 * np.max(score):.2f}% keyakinan)"
            )
        else:
            st.error("Model klasifikasi belum berhasil dimuat.")

# ==========================
# ERROR HANDLER
# ==========================
if load_err:
    st.sidebar.error(f"⚠️ Gagal memuat model: {load_err}")
