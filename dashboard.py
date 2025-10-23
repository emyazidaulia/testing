import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import random 

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']
# PNG_URL_DETECT = "https://raw.githubusercontent.com/emyazidaulia/testing/main/sample_images/00000058.png" # 🚨 DIHAPUS
IMG_URLS_HOME = [
    "https://i.imgur.com/iTMrNAj.jpeg",
    "https://i.imgur.com/FsTtNpE.jpeg",
    "https://i.imgur.com/DEqLHqH.gif",
    "https://i.imgur.com/VwBdFtX.jpeg"
]
TOTAL_DURATION = 20
# IMAGE_COUNT_DETECT = 5 # Diganti dengan EMOJI_COUNT_DETECT
EMOJI_COUNT_CLASSIFY = 40 
EMOJIS_CLASSIFY = ["🔥", "🌲"] 

# 🚨 BARU: Konfigurasi untuk Deteksi Objek
EMOJI_COUNT_DETECT = 30 # Jumlah emoji catur yang akan bergerak
EMOJIS_CHESS = ["♜", "♞", "♝", "♛", "♚", "♟"] # Emoji bidak catur


# =======================================================
# 1. FUNGSI STYLE CSS GLOBAL (Diperbarui untuk Animasi Emoji Catur)
# =======================================================
def set_global_styles():
    css_global = f"""
    <style>
    /* ... (Style umum tidak berubah) ... */
    
    .main, .stApp {{ background: none !important; }}
    
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

    /* 🚨 LAMA: KEYFRAMES PERGERAKAN HORIZONTAL UNTUK GAMBAR (Deteksi) - Akan diubah */
    /* 🚨 BARU: KEYFRAMES UNTUK EMOJI CATUR (Deteksi) - Pergerakan Acak */
    @keyframes move-and-spin-chess-emoji {{ 
        0% {{ 
            transform: translate(0, 0) rotate(0deg) scale(0.6); 
            opacity: 0;
        }} 
        30% {{
            transform: translate(-20vw, 30vh) rotate(180deg) scale(0.9);
            opacity: 0.7; 
        }}
        70% {{
            transform: translate(60vw, -40vh) rotate(540deg) scale(1.2);
            opacity: 0.7;
        }}
        100% {{ 
            transform: translate(120vw, 80vh) rotate(720deg) scale(0.6); 
            opacity: 0; 
        }} 
    }}

    /* KEYFRAMES UNTUK EMOJI API (Klasifikasi) */
    @keyframes move-and-spin-emoji {{ 
        0% {{ 
            transform: translate(0, 0) rotate(0deg) scale(0.5); 
            opacity: 0;
        }} 
        30% {{
            transform: translate(25vw, -30vh) rotate(180deg) scale(0.8);
            opacity: 0.7; 
        }}
        70% {{
            transform: translate(75vw, 50vh) rotate(540deg) scale(1.1);
            opacity: 0.7;
        }}
        100% {{ 
            transform: translate(100vw, 100vh) rotate(720deg) scale(0.5); 
            opacity: 0; 
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
    
    /* 🚨 DIHAPUS: Style untuk Container Gambar Deteksi */
    /* 🚨 BARU: Style untuk Layer Emoji Catur (Deteksi) */
    .chess-emoji-layer {{
        position: fixed; 
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -2; 
        pointer-events: none;
        overflow: hidden; 
        font-size: 0; 
    }}
    
    /* 🚨 BARU: Style untuk Setiap Emoji Catur */
    .chess-emoji-layer span {{
        position: absolute;
        font-size: 60px; /* Ukuran emoji catur */
        opacity: 0; 
        animation: move-and-spin-chess-emoji 20s infinite ease-in-out; /* Durasi animasi catur */
        display: block;
        line-height: 1;
        filter: drop-shadow(0 0 5px rgba(0, 0, 0, 0.7)); /* Bayangan lebih kuat untuk catur */
    }}

    /* Style untuk Layer Emoji Api (Klasifikasi) */
    .fire-emoji-layer {{
        position: fixed; 
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -2; 
        pointer-events: none;
        overflow: hidden; 
        font-size: 0; 
    }}
    
    /* Style untuk Setiap Emoji Api */
    .fire-emoji-layer span {{
        position: absolute;
        font-size: 50px; 
        opacity: 0; 
        animation: move-and-spin-emoji 15s infinite ease-in-out; 
        display: block;
        line-height: 1;
        filter: drop-shadow(0 0 4px rgba(0, 0, 0, 0.5));
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
        
    elif page == "classify":
        # --- GENERATE MULTIPLE MOVING EMOJI (Klasifikasi) ---
        emojis_html = ""
        
        for i in range(EMOJI_COUNT_CLASSIFY):
            left_percent = random.randint(-20, 100) 
            top_percent = random.randint(0, 100) 
            
            duration = random.uniform(8, 12) 
            delay = random.uniform(0, 8) 
            
            selected_emoji = random.choice(EMOJIS_CLASSIFY)
            
            emojis_html += f'<span style="left: {left_percent}%; top: {top_percent}%; animation-duration: {duration:.2f}s; animation-delay: {delay:.2f}s;">{selected_emoji}</span>'
        
        html_markup = f'<div class="fire-emoji-layer">{emojis_html}</div>'
        st.markdown(html_markup, unsafe_allow_html=True)
        
    elif page == "detect":
        # 🚨 BARU: GENERATE MULTIPLE MOVING CHESS EMOJI (Deteksi)
        chess_emojis_html = ""
        for i in range(EMOJI_COUNT_DETECT):
            left_percent = random.randint(-20, 100) # Mulai dari kiri luar sampai kanan
            top_percent = random.randint(0, 100) # Mulai dari atas sampai bawah
            
            duration = random.uniform(15, 25) # Durasi animasi catur sedikit lebih lambat
            delay = random.uniform(0, 10) # Delay acak
            
            selected_chess_emoji = random.choice(EMOJIS_CHESS)
            
            chess_emojis_html += f'<span style="left: {left_percent}%; top: {top_percent}%; animation-duration: {duration:.2f}s; animation-delay: {delay:.2f}s;">{selected_chess_emoji}</span>'
        
        html_markup = f'<div class="chess-emoji-layer">{chess_emojis_html}</div>'
        st.markdown(html_markup, unsafe_allow_html=True)


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
# Halaman HOME
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
# Halaman KLASIFIKASI (dengan background emoji api & pohon beterbangan)
# ==========================
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")
    
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) 

    # ... (sisa konten klasifikasi)
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
# Halaman DETEKSI (dengan background emoji catur beterbangan)
# ==========================
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # Tambahkan spasi di atas konten

    # ... (sisa konten deteksi)
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
