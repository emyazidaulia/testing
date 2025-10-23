import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# KONFIGURASI GLOBAL
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']

st.set_page_config(page_title="Dashboard Deteksi & Klasifikasi", layout="wide")

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
# NAVIGASI
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

with st.sidebar:
    st.title("📍 Navigasi")
    st.button("🏠 Home", on_click=lambda: go_to("home"))
    st.button("🧩 Deteksi Objek", on_click=lambda: go_to("deteksi"))
    st.button("🖼️ Klasifikasi Gambar", on_click=lambda: go_to("klasifikasi"))
    if load_err:
        st.error(f"⚠️ Model error: {load_err}")
    else:
        st.success("✅ Model siap digunakan")

# ==========================
# HALAMAN HOME (DENGAN BACKGROUND ANIMASI)
# ==========================
if st.session_state.page == "home":
    background_images = [
        "https://i.imgur.com/iTMrNAj.jpeg",
        "https://i.imgur.com/FsTtNpE.jpeg",
        "https://i.imgur.com/DEqLHqH.gif",
        "https://i.imgur.com/VwBdFtX.jpeg"
    ]

    st.markdown(f"""
        <style>
        .stApp {{
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            animation: changeBackground 25s infinite ease-in-out;
            transition: background-image 1s ease-in-out;
        }}
        @keyframes changeBackground {{
            0%   {{ background-image: url('{background_images[0]}'); }}
            25%  {{ background-image: url('{background_images[1]}'); }}
            50%  {{ background-image: url('{background_images[2]}'); }}
            75%  {{ background-image: url('{background_images[3]}'); }}
            100% {{ background-image: url('{background_images[0]}'); }}
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style='text-align:center; color:white; text-shadow:2px 2px 8px black'>
            🌍 Dashboard Deteksi & Klasifikasi Gambar
        </h1>
        <p style='text-align:center; color:white; font-size:18px;'>
            Selamat datang! Gunakan sidebar untuk menjelajahi fitur.  
            Background ini berganti otomatis ✨
        </p>
    """, unsafe_allow_html=True)

# ==========================
# HALAMAN DETEKSI OBJEK (DENGAN ANIMASI BIDAK CATUR)
# ==========================
elif st.session_state.page == "deteksi":
    # Buat background polos
    st.markdown(
        "<style>.stApp {background-color: #f9f9f9 !important; background-image: none !important;}</style>",
        unsafe_allow_html=True
    )

    # Tambahkan animasi bidak catur
    st.markdown("""
        <style>
        .chess-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            overflow: hidden;
            z-index: -1;
            pointer-events: none;
        }

        .chess-piece {
            position: absolute;
            width: 70px;
            opacity: 0.4;
            animation-timing-function: linear;
            filter: drop-shadow(0 0 5px rgba(0,0,0,0.3));
        }

        /* Gerak horizontal */
        @keyframes moveAcross {
            0% { left: -10%; }
            100% { left: 110%; }
        }

        /* Gerak vertikal lembut */
        @keyframes floatPiece {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-30px) rotate(10deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        </style>

        <div class="chess-bg">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Chess_Piece_-_King_White.svg"
                 class="chess-piece" style="top:10%; animation: moveAcross 25s infinite, floatPiece 4s infinite ease-in-out;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_Piece_-_Queen_Black.svg"
                 class="chess-piece" style="top:30%; animation: moveAcross 30s infinite 3s, floatPiece 5s infinite ease-in-out;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Chess_Piece_-_Rook_White.svg"
                 class="chess-piece" style="top:50%; animation: moveAcross 28s infinite 5s, floatPiece 4.5s infinite ease-in-out;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Chess_Piece_-_Bishop_Black.svg"
                 class="chess-piece" style="top:65%; animation: moveAcross 24s infinite 8s, floatPiece 5s infinite ease-in-out;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_Piece_-_Knight_White.svg"
                 class="chess-piece" style="top:80%; animation: moveAcross 27s infinite 10s, floatPiece 6s infinite ease-in-out;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Chess_Piece_-_Pawn_Black.svg"
                 class="chess-piece" style="top:90%; animation: moveAcross 22s infinite 12s, floatPiece 4s infinite ease-in-out;">
        </div>
    """, unsafe_allow_html=True)

    # Judul halaman
    st.title("🎯 Deteksi Objek (Bidak Catur Bergerak)")
    st.write("Unggah gambar untuk mendeteksi objek menggunakan model YOLO.")

    uploaded_file = st.file_uploader("Pilih gambar untuk dideteksi...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Gambar yang diunggah", use_container_width=True)

        if yolo_model:
            results = yolo_model(img)
            result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
        else:
            st.error("⚠️ Model YOLO belum berhasil dimuat.")

# ==========================
# HALAMAN KLASIFIKASI
# ==========================
elif st.session_state.page == "klasifikasi":
    # Background polos
    st.markdown(
        "<style>.stApp {background-color: white !important; background-image: none !important;}</style>",
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
            st.success(f"Hasil Prediksi: **{CLASS_NAMES[np.argmax(score)]}** ({100 * np.max(score):.2f}% keyakinan)")
        else:
            st.error("⚠️ Model klasifikasi belum berhasil dimuat.")
