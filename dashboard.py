import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']

# ==========================
# Custom CSS untuk Animated Background
# ==========================
def set_animated_background():
    IMG_URLS = [
        "https://i.imgur.com/iTMrNAj.jpeg",
        "https://i.imgur.com/FsTtNpE.jpeg",
        "https://i.imgur.com/DEqLHqH.gif",
        "https://i.imgur.com/VwBdFtX.jpeg"
    ]
    TOTAL_DURATION = 20

    css_animation = f"""
    <style>
    .main, .stApp {{
        background: none !important;
    }}
    .stApp:before {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        animation: image-swap {TOTAL_DURATION}s infinite;
        background-size: cover;
        background-position: center;
        opacity: 0.5;
        transition: background-image 1s ease-in-out, opacity 1s ease-in-out;
    }}
    [data-testid="stAppViewBlockContainer"] {{
        background: rgba(14,17,23,0.7) !important;
        backdrop-filter: blur(2px);
        border-radius: 10px;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(14,17,23,0.9) !important;
    }}
    .stApp button[kind="secondary"] {{
        background-color: #003366 !important;
        color: white !important;
        border-color: #003366 !important;
    }}
    @keyframes image-swap {{
        0%,20% {{ background-image: url('{IMG_URLS[0]}'); }}
        25%,45% {{ background-image: url('{IMG_URLS[1]}'); }}
        50%,70% {{ background-image: url('{IMG_URLS[2]}'); }}
        75%,95% {{ background-image: url('{IMG_URLS[3]}'); }}
        100% {{ background-image: url('{IMG_URLS[0]}'); }}
    }}
    </style>
    """
    st.markdown(css_animation, unsafe_allow_html=True)

set_animated_background()

# ==========================
# Load Models
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
# Konfigurasi Halaman
# ==========================
st.set_page_config(page_title="Image Classifier & Detection", layout="wide")

# ==========================
# Navigasi
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

with st.sidebar:
    st.title("🔍 Menu Navigasi")
    st.button("🏠 Home", key="nav_home", on_click=go_to, args=("home",), use_container_width=True)
    st.button("🖼 Klasifikasi Gambar", key="nav_classify", on_click=go_to, args=("classify",), use_container_width=True)
    st.button("🎯 Deteksi Objek", key="nav_detect", on_click=go_to, args=("detect",), use_container_width=True)
    
    if load_err:
        st.error(f"❌ Model Error: {load_err[:50]}...")
    elif yolo_model is None or classifier is None:
        st.warning("⚠️ Salah satu atau kedua model gagal dimuat.")
    else:
        st.success("✅ Model siap digunakan.")

# ==========================
# Halaman HOME
# ==========================
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center; color:white;'>Analisis Gambar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.header("🔥 Klasifikasi Gambar Hutan")
            st.write("Klasifikasikan gambar menjadi **Kebakaran Hutan** atau **Bukan Kebakaran Hutan**.")
            st.button("➡️ Mulai Klasifikasi", key="home_classify", on_click=go_to, args=("classify",), use_container_width=True, type="primary")

    with col2:
        with st.container(border=True):
            st.header("♞ Deteksi Bidak Catur")
            st.write("Deteksi posisi bidak catur pada gambar.")
            st.button("➡️ Mulai Deteksi", key="home_detect", on_click=go_to, args=("detect",), use_container_width=True)

# ==========================
# Halaman KLASIFIKASI
# ==========================
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif classifier is None:
        st.warning("Model Klasifikasi tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            if st.button('Lakukan Klasifikasi', type="primary"):
                with st.spinner('Memproses...'):
                    img_resized = img.resize((128, 128))
                    img_array = image.img_to_array(img_resized)
                    img_array = np.expand_dims(img_array, axis=0) / 255.0
                    prediction = classifier.predict(img_array)
                    class_index = np.argmax(prediction)
                    probability = np.max(prediction)

                    st.markdown("---")
                    predicted_class = CLASS_NAMES[class_index]
                    if predicted_class == 'Kebakaran Hutan':
                        st.error("🔥 **Terdeteksi: Kebakaran Hutan**")
                    else:
                        st.success("🏡 **Terdeteksi: Bukan Kebakaran Hutan**")
                    st.write(f"Tingkat Keyakinan: **{probability*100:.2f}%**")

    st.markdown("---")
    st.button("⬅ Kembali", key="back_classify", on_click=go_to, args=("home",))

# ==========================
# Halaman DETEKSI
# ==========================
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")

    # ===== Animasi Bidak Catur =====
    st.markdown("""
    <style>
    .chess-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        overflow: hidden;
        z-index: -2;
        pointer-events: none;
    }
    .piece {
        position: absolute;
        width: 60px;
        opacity: 0.35;
        animation: floatPiece 3s ease-in-out infinite alternate, moveAcross linear infinite;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.3));
    }
    @keyframes floatPiece {
        from { transform: translateY(0px) rotate(0deg); }
        to { transform: translateY(-20px) rotate(10deg); }
    }
    @keyframes moveAcross {
        from { left: -10%; }
        to { left: 110%; }
    }
    </style>

    <div class="chess-bg">
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Chess_Piece_-_King_White.svg" class="piece" style="top: 10%; animation-duration: 25s;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_Piece_-_Queen_Black.svg" class="piece" style="top: 30%; animation-duration: 28s; animation-delay: 5s;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Chess_Piece_-_Rook_White.svg" class="piece" style="top: 50%; animation-duration: 30s; animation-delay: 10s;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Chess_Piece_-_Bishop_Black.svg" class="piece" style="top: 65%; animation-duration: 26s; animation-delay: 15s;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_Piece_-_Knight_White.svg" class="piece" style="top: 80%; animation-duration: 32s; animation-delay: 8s;">
    </div>
    """, unsafe_allow_html=True)

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif yolo_model is None:
        st.warning("Model Deteksi tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            if st.button('Lakukan Deteksi', type="primary"):
                with st.spinner('Memproses Deteksi...'):
                    results = yolo_model(img)
                    result_img = results[0].plot()

                    detected_labels = []
                    if hasattr(results[0], "boxes"):
                        for box in results[0].boxes:
                            class_id = int(box.cls[0]) if hasattr(box.cls, "__getitem__") else int(box.cls)
                            label = results[0].names.get(class_id, str(class_id))
                            detected_labels.append(label)

                    st.markdown("---")
                    st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
                    if detected_labels:
                        unique_labels = list(dict.fromkeys(detected_labels))
                        st.success(f"🧩 Objek Terdeteksi: {', '.join(unique_labels)}")
                    else:
                        st.warning("Tidak ada objek yang terdeteksi.")

    st.markdown("---")
    st.button("⬅ Kembali", key="back_detect", on_click=go_to, args=("home",))
