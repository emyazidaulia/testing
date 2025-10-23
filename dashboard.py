import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan'] # sesuaikan

# URL gambar PNG baru
PNG_URL_DETECT = "https://raw.githubusercontent.com/emyazidaulia/testing/main/sample_images/00000058.png"

# ==========================
# Fungsi Background Animasi Global
# ==========================
def set_global_styles():
    IMG_URLS = [
        "https://i.imgur.com/iTMrNAj.jpeg",
        "https://i.imgur.com/FsTtNpE.jpeg",
        "https://i.imgur.com/DEqLHqH.gif",
        "https://i.imgur.com/VwBdFtX.jpeg"
    ]
    TOTAL_DURATION = 20
    
    css_animation = f"""
    <style>
    /* RESET BACKGROUND BAWAAN STREAMLIT */
    .main, .stApp {{ background: none !important; }}
    
    /* STYLE TRANSPARANSI KONTEN UTAMA */
    [data-testid="stAppViewBlockContainer"] {{
        background: rgba(14, 17, 23, 0.7) !important;
        backdrop-filter: blur(2px);
        border-radius: 10px;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(14, 17, 23, 0.9) !important;
    }}
    
    /* STYLE TOMBOL KHUSUS (Biru Tua) */
    .stApp button[kind="secondary"] {{
        background-color: #003366 !important;
        color: white !important;
        border-color: #003366 !important;
    }}
    
    /* 1. LAYER HOME BACKGROUND (IMAGE SWAP) */
    .home-bg {{
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
        display: none; 
    }}
    
    /* 2. LAYER DETECT BACKGROUND (GAMBAR PNG BERGERAK) */
    .detect-bg {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        background-image: url('{PNG_URL_DETECT}');
        background-size: 20%; /* Ukuran gambar yang kecil */
        background-repeat: no-repeat;
        background-position: top left;
        opacity: 0.25; /* Transparansi agar tidak mengganggu */
        animation: move-and-fade 15s ease-in-out infinite alternate; 
        display: none; 
    }}

    /* KEYFRAMES UNTUK HOME BG */
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
    
    /* KEYFRAMES UNTUK DETECT BG (BERGERAK & MEMUDAR) */
    @keyframes move-and-fade {{ 
        0% {{ background-position: 5% 10%; opacity: 0.15; transform: scale(1); }} 
        50% {{ background-position: 50% 90%; opacity: 0.35; transform: scale(1.1); }} 
        100% {{ background-position: 95% 10%; opacity: 0.15; transform: scale(1); }} 
    }}
    </style>
    
    <div class="home-bg" id="animated-home-bg"></div>

    <div class="detect-bg" id="animated-detect-bg"></div>
    """
    st.markdown(css_animation, unsafe_allow_html=True)

# Panggil fungsi CSS global hanya sekali di awal
set_global_styles()

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
# FUNGSI UNTUK MENGAKTIFKAN/MENONAKTIFKAN BACKGROUND
# ==========================
def toggle_bg(home_active=False, detect_active=False):
    # Menggunakan Javascript untuk mengubah style elemen HTML yang kita injeksi
    js_code = f"""
    <script>
    var homeBg = document.getElementById('animated-home-bg');
    var detectBg = document.getElementById('animated-detect-bg');
    if (homeBg) homeBg.style.display = '{'block' if home_active else 'none'}';
    if (detectBg) detectBg.style.display = '{'block' if detect_active else 'none'}';
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# ==========================
# Halaman HOME (dengan background animasi gambar)
# ==========================
if st.session_state.page == "home":
    toggle_bg(home_active=True, detect_active=False) # Aktifkan latar belakang gambar (Home)

    st.markdown("<h1 style='text-align:center; color:#FFFFFF; text-shadow: 2px 2px 4px #000000;'>🔥 Aplikasi Analisis Kebakaran Hutan</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 18px; color: white; text-shadow: 1px 1px 3px #000000;'>Pilih salah satu layanan analitik di bawah untuk memulai pemrosesan gambar Anda.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_classify, col_detect = st.columns(2)

    with col_classify:
        with st.container(border=True):
            st.header("🖼 Klasifikasi Gambar")
            st.caption("Cek Tipe Gambar")
            st.write("Sistem akan mengklasifikasikan gambar yang Anda unggah sebagai **'Kebakaran Hutan'** atau **'Bukan Kebakaran Hutan'**.")
            st.button("➡️ Mulai Klasifikasi", key="home_open_classify_unique", on_click=go_to, args=("classify",), use_container_width=True, type="primary")

    with col_detect:
        with st.container(border=True):
            st.header("🎯 Deteksi Objek")
            st.caption("Temukan Lokasi Spesifik")
            st.write("Sistem akan mendeteksi dan menandai **api** atau **asap** di dalam gambar, memberikan *bounding box* hasil deteksi.")
            st.button("➡️ Mulai Deteksi Objek", key="home_open_detect_unique", on_click=go_to, args=("detect",), use_container_width=True)

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


# ==========================
# Halaman KLASIFIKASI (background polos)
# ==========================
elif st.session_state.page == "classify":
    toggle_bg(home_active=False, detect_active=False) # Matikan semua latar belakang kustom

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
# Halaman DETEKSI (background gambar PNG bergerak)
# ==========================
elif st.session_state.page == "detect":
    toggle_bg(home_active=False, detect_active=True) # Aktifkan latar belakang gambar PNG (Detect)

    st.header("🎯 Menu Deteksi Objek")

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
