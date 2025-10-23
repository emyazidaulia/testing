import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']  # sesuaikan

# ==========================
# Fungsi Background Animasi (KHUSUS HOME)
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
        background: rgba(14, 17, 23, 0.7) !important;
        backdrop-filter: blur(2px);
        border-radius: 10px;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(14, 17, 23, 0.9) !important;
    }}
    .stApp button[kind="secondary"] {{
        background-color: #003366 !important;
        color: white !important;
        border-color: #003366 !important;
    }}
    @keyframes image-swap {{
        0% {{ background-image: url('{IMG_URLS[0]}'); }}
        20% {{ background-image: url('{IMG_URLS[0]}'); }}
        24% {{ opacity: 0.2; }}
        25% {{ background-image: url('{IMG_URLS[1]}'); opacity: 0.5; }}
        45% {{ background-image: url('{IMG_URLS[1]}'); }}
        49% {{ opacity: 0.2; }}
        50% {{ background-image: url('{IMG_URLS[2]}'); opacity: 0.5; }}
        70% {{ background-image: url('{IMG_URLS[2]}'); }}
        74% {{ opacity: 0.2; }}
        75% {{ background-image: url('{IMG_URLS[3]}'); opacity: 0.5; }}
        95% {{ background-image: url('{IMG_URLS[3]}'); }}
        99% {{ opacity: 0.2; }}
        100% {{ background-image: url('{IMG_URLS[0]}'); opacity: 0.5; }}
    }}
    </style>
    """
    st.markdown(css_animation, unsafe_allow_html=True)


# ==========================
# Load Models (basecode)
# ==========================
@st.cache_resource
def load_models():
    try:
        yolo_model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")
        classifier = tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")
        return yolo_model, classifier
    except Exception as e:
        return None, None, str(e)

models = load_models()
if isinstance(models, tuple) and len(models) == 3:
    yolo_model, classifier, load_err = models
else:
    try:
        yolo_model, classifier = models
        load_err = None
    except Exception:
        yolo_model, classifier, load_err = None, None, "Unknown error saat memuat model."


# ==========================
# Konfigurasi Halaman
# ==========================
st.set_page_config(page_title="Image Classifier & Detection", layout="wide")

# ==========================
# Navigasi (Session State)
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# ==========================
# Sidebar Navigasi
# ==========================
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
# Halaman HOME (dengan background animasi)
# ==========================
if st.session_state.page == "home":
    set_animated_background()  # <── hanya aktif di halaman home

    st.markdown("<h1 style='text-align:center; color:#FFFFFF; text-shadow: 2px 2px 4px #000000;'>Analisis Gambar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 18px; color: white; text-shadow: 1px 1px 3px #000000;'>Pilih salah satu pilihan di bawah untuk memulai pemrosesan gambar Anda.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_classify, col_detect = st.columns(2)

    with col_classify:
        with st.container(border=True):
            st.header("🔥 Klasifikasi Gambar Hutan")
            st.caption("Cek Tipe Gambar")
            st.write("Sistem akan mengklasifikasikan gambar yang Anda unggah sebagai **'Kebakaran Hutan'** atau **'Bukan Kebakaran Hutan'**.")
            st.button("➡️ Mulai Klasifikasi", key="home_open_classify_unique", on_click=go_to, args=("classify",), use_container_width=True, type="primary")

    with col_detect:
        with st.container(border=True):
            st.header("♞ Deteksi Bidak Catur")
            st.caption("Temukan Lokasi Spesifik")
            st.write("Sistem akan mendeteksi dan menandai bidak catur di dalam gambar, memberikan *bounding box* hasil deteksi.")
            st.button("➡️ Mulai Deteksi Objek", key="home_open_detect_unique", on_click=go_to, args=("detect",), use_container_width=True)

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


# ==========================
# Halaman KLASIFIKASI (background polos)
# ==========================
elif st.session_state.page == "classify":
    st.markdown("<style>.stApp:before {content:none !important; background:none !important;}</style>", unsafe_allow_html=True)
    st.header("🖼 Menu Klasifikasi Gambar")

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif classifier is None:
        st.warning("Model Klasifikasi tidak dapat dimuat. Cek jalur file model (.h5) Anda.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)
            if st.button('Lakukan Klasifikasi', type="primary", use_container_width=True):
                with st.spinner('Memproses Klasifikasi...'):
                    img_resized = img.resize((128, 128))
                    img_array = image.img_to_array(img_resized)
                    img_array = np.expand_dims(img_array, axis=0) / 255.0
                    prediction = classifier.predict(img_array)
                    class_index = np.argmax(prediction)
                    probability = np.max(prediction)
                st.markdown("---")
                if class_index < len(CLASS_NAMES):
                    predicted_class = CLASS_NAMES[class_index]
                    if predicted_class == 'Kebakaran Hutan':
                        st.error("🔥 **[HASIL KRITIS]** Terdeteksi: Kebakaran Hutan")
                    else:
                        st.success("🏡 **[HASIL AMAN]** Terdeteksi: Bukan Kebakaran Hutan")
                    st.markdown(f"### Kelas Prediksi: **{predicted_class}**")
                    st.write(f"Tingkat Keyakinan: **{probability*100:.2f}%**")
                else:
                    st.error("Indeks kelas tidak valid. Pastikan CLASS_NAMES sudah benar.")
                st.markdown("---")
                st.button("⬅ Kembali ke Home", key="back_from_classify", on_click=go_to, args=("home",))


# ==========================
# Halaman DETEKSI (polos + animasi bidak catur)
# ==========================
elif st.session_state.page == "detect":
    st.markdown("<style>.stApp:before {content:none !important; background:none !important;}</style>", unsafe_allow_html=True)
    st.header("🎯 Menu Deteksi Objek")

    # Animasi bidak catur bergerak
    st.markdown("""
    <style>
    .chess-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; z-index: -2; pointer-events: none; }
    .piece { position: absolute; width: 60px; opacity: 0.35; animation: floatPiece linear infinite; filter: drop-shadow(0 0 5px rgba(255,255,255,0.3)); }
    @keyframes floatPiece { 0% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-25px) rotate(10deg); } 100% { transform: translateY(0px) rotate(0deg); } }
    @keyframes moveAcross { 0% { left: -10%; } 100% { left: 110%; } }
    </style>
    <div class="chess-bg">
      <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Chess_Piece_-_King_White.svg" class="piece" style="top: 10%; animation: moveAcross 25s linear infinite, floatPiece 4s ease-in-out infinite;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_Piece_-_Queen_Black.svg" class="piece" style="top: 30%; animation: moveAcross 30s linear infinite 5s, floatPiece 5s ease-in-out infinite;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Chess_Piece_-_Rook_White.svg" class="piece" style="top: 50%; animation: moveAcross 28s linear infinite 8s, floatPiece 4s ease-in-out infinite;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Chess_Piece_-_Bishop_Black.svg" class="piece" style="top: 65%; animation: moveAcross 22s linear infinite 2s, floatPiece 5s ease-in-out infinite;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_Piece_-_Knight_White.svg" class="piece" style="top: 80%; animation: moveAcross 32s linear infinite 10s, floatPiece 4s ease-in-out infinite;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Chess_Piece_-_Pawn_Black.svg" class="piece" style="top: 90%; animation: moveAcross 26s linear infinite 12s, floatPiece 5s ease-in-out infinite;">
    </div>
    """, unsafe_allow_html=True)

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif yolo_model is None:
        st.warning("Model Deteksi Objek tidak dapat dimuat. Cek jalur file model (.pt) Anda.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)
            if st.button('Lakukan Deteksi', type="primary", use_container_width=True):
                with st.spinner('Memproses Deteksi Objek...'):
                    results = yolo_model(img)
                    result_img = results[0].plot()
                    detected_labels = []
                    if hasattr(results[0], "boxes") and results[0].boxes is not None:
                        for box in results[0].boxes:
                            try:
                                class_id = int(box.cls[0])
                            except Exception:
                                class_id = int(box.cls)
                            label = results[0].names.get(class_id, str(class_id)) if hasattr(results[0], "names") else str(class_id)
                            detected_labels.append(label)

                st.markdown("---")
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
                st.success("✅ Deteksi Selesai!")

                if detected_labels:
                    unique_labels = list(dict.fromkeys(detected_labels))
                    label_text = ", ".join(unique_labels)
                    total = len(detected_labels)
                    st.markdown(f"### 🧩 Objek Terdeteksi: **{label_text}**")
                    st.write(f"Jumlah total kotak objek terdeteksi: **{total}**")
                else:
                    st.warning("Tidak ada objek yang terdeteksi.")

                st.markdown("---")
                st.button("⬅ Kembali ke Home", key="back_from_detect", on_click=go_to, args=("home",))
