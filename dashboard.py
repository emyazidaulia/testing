import streamlit as st
from streamlit_lottie import st_lottie
import requests 
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']
PNG_URL_DETECT = "https://raw.githubusercontent.com/emyazidaulia/testing/main/sample_images/00000058.png"
IMG_URLS_HOME = [
    "https://i.imgur.com/iTMrNAj.jpeg",
    "https://i.imgur.com/FsTtNpE.jpeg",
    "https://i.imgur.com/DEqLHqH.gif",
    "https://i.imgur.com/VwBdFtX.jpeg"
]
TOTAL_DURATION = 20
IMAGE_COUNT = 5 
LOTTIE_FIRE_URL = "https://lottie.host/86581997-293e-48ac-b09e-73c3397984f4/T012Yk7w0y.json" 

# =======================================================
# Fungsi Bantuan untuk Lottie
# =======================================================
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# =======================================================
# 1. FUNGSI STYLE CSS GLOBAL (Dibersihkan dari Lottie CSS)
# =======================================================
def set_global_styles():
    css_global = f"""
    <style>
    /* RESET UTAMA: Mengatur konten utama dan sidebar agar transparan */
    .main, .stApp {{ background: none !important; }}
    
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

    /* KEYFRAMES UNTUK HOME BG (Gambar berganti-ganti) */
    @keyframes image-swap {{
        0% {{ background-image: url('{IMG_URLS_HOME[0]}'); }}
        20% {{ background-image: url('{IMG_URLS_HOME[0]}'); }}
        24% {{ opacity: 0.2; }}
        25% {{ background-image: url('{IMG_URLS_HOME[1]}'); opacity: 0.5; }}
        45% {{ background-image: url('{IMG_URLS_HOME[1]}'); }}
        49% {{ opacity: 0.2; }}
        50% {{ background-image: url('{IMG_URLS_HOME[2]}'); opacity: 0.5; }}
        70% {{ background-image: url('{IMG_URLS_HOME[2]}'); }}
        74% {{ opacity: 0.2; }}
        75% {{ background-image: url('{IMG_URLS_HOME[3]}'); opacity: 0.5; }}
        95% {{ background-image: url('{IMG_URLS_HOME[3]}'); }}
        99% {{ opacity: 0.2; }}
        100% {{ background-image: url('{IMG_URLS_HOME[0]}'); opacity: 0.5; }}
    }}

    /* KEYFRAMES PERGERAKAN HORIZONTAL (Kiri ke Kanan) */
    @keyframes move-and-fade {{ 
        0% {{ 
            transform: translateX(-100%) scale(1); 
            opacity: 0.2;
        }} 
        100% {{ 
            transform: translateX(100vw) scale(1.1); 
            opacity: 0.4; 
        }} 
    }}

    /* Style untuk Latar Belakang Home */
    .home-bg-layer {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1; 
        background-size: cover;
        background-position: center;
        opacity: 0.5;
        animation: image-swap {TOTAL_DURATION}s infinite;
    }}
    
    /* Style untuk Container Gambar Deteksi */
    .detect-img-layer {{
        position: fixed; 
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -2; /* Di depan layer gelap global (-3) */
        pointer-events: none;
        overflow: hidden; 
        line-height: 0;
        font-size: 0;
    }}
    
    /* Style untuk Setiap Gambar */
    .detect-img-layer img {{
        width: 100px; 
        position: absolute;
        opacity: 0.25; 
        animation: move-and-fade 25s linear infinite; 
        filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.1));
    }}
    
    </style>
    """
    st.markdown(css_global, unsafe_allow_html=True)

# Panggil fungsi CSS global hanya sekali di awal
set_global_styles()


# =======================================================
# 2. FUNGSI UNTUK MENGAKTIFKAN BACKGROUND SESUAI HALAMAN
# =======================================================
def render_background_layer(page):
    # Rendam layer background gelap global (digunakan di semua halaman)
    st.markdown('<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.2); z-index: -3;"></div>', unsafe_allow_html=True)

    if page == "home":
        st.markdown(f'<div class="home-bg-layer"></div>', unsafe_allow_html=True)
        
    elif page == "detect":
        # --- GENERATE MULTIPLE MOVING IMAGES ---
        images_html = ""
        for i in range(IMAGE_COUNT):
            top_percent = 10 + (i * 15) 
            duration = 25 + (i * 2) 
            delay = i * 5 
            
            images_html += f"""<img 
                src="{PNG_URL_DETECT}" 
                alt="Moving Object {i+1}" 
                style="
                    top: {top_percent}%; 
                    animation-duration: {duration}s;
                    animation-delay: {delay}s;
                ">"""
        
        # Injeksi gambar bergerak (detect-img-layer z-index: -2)
        html_markup = f"""<div class="detect-img-layer">{images_html}</div>"""
        st.markdown(html_markup, unsafe_allow_html=True)
        
    # Halaman Klasifikasi tidak memiliki background fixed, Lottie akan ditampilkan di dalam konten utama.


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

# =======================================================
# KONTEN HALAMAN UTAMA
# =======================================================

# Rendam layer background yang sesuai sebelum konten halaman
render_background_layer(st.session_state.page)

# ==========================
# Halaman HOME (dengan background animasi gambar)
# ==========================
if st.session_state.page == "home":
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
# Halaman KLASIFIKASI (dengan Lottie di dalam konten)
# ==========================
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")
    
    # 🚨 PERBAIKAN DI SINI: Tampilkan Lottie di atas, menggunakan st.columns
    lottie_json = load_lottieurl(LOTTIE_FIRE_URL)
    if lottie_json:
        col_lottie_1, col_lottie_main, col_lottie_2 = st.columns([1, 2, 1])
        with col_lottie_main:
            st_lottie(
                lottie_json,
                speed=1,
                reverse=False,
                loop=True,
                quality="low", 
                height=200, # Ukuran yang lebih wajar
                key="fire_animation",
            )
    
    # ... (sisa konten klasifikasi)
    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif classifier is None:
        st.warning("Model Klasifikasi tidak dapat dimuat. Cek jalur file model (.h5) Anda.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])
        # ... (lanjutan kode klasifikasi tidak berubah)
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
    st.header("🎯 Menu Deteksi Objek")
    
    # ... (sisa konten deteksi)
    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif yolo_model is None:
        st.warning("Model Deteksi Objek tidak dapat dimuat. Cek jalur file model (.pt) Anda.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
        # ... (lanjutan kode deteksi tidak berubah)
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
