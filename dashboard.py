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
# Custom CSS untuk Animated Background (DIPERBAIKI)
# ==========================

def set_animated_background():
    # Link gambar yang Anda berikan
    IMG_URLS = [
        "https://i.imgur.com/iTMrNAj.jpeg",  # Gambar 1
        "https://i.imgur.com/FsTtNpE.jpeg",  # Gambar 2
        "https://i.imgur.com/DEqLHqH.gif",   # Gambar 3 (GIF)
        "https://i.imgur.com/VwBdFtX.jpeg"   # Gambar 4
    ]
    
    TOTAL_DURATION = 20
    
    css_animation = f"""
    <style>
    /* 1. MENGATASI LATAR BELAKANG STREAMLIT BAWAAN */
    /* Menghapus latar belakang bawaan dari elemen root (body dan stApp) */
    .main {{
        background: none !important;
    }}
    .stApp {{
        background: none !important;
    }}

    /* 2. MEMBUAT LAPISAN LATAR BELAKANG BERANIMASI PADA LEVEL ROOT */
    .stApp:before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1; /* Jauh di belakang semua konten */
        animation: image-swap {TOTAL_DURATION}s infinite; 
        background-size: cover;
        background-position: center;
        opacity: 0.5; /* Opacity rendah agar konten mudah dibaca */
        transition: background-image 1s ease-in-out, opacity 1s ease-in-out;
    }}

    /* 3. MEMASTIKAN KONTEN UTAMA CUKUP TRANSPARAN */
    /* Konten utama: Hapus background bawaan Streamlit (hitam/putih) */
    [data-testid="stAppViewBlockContainer"] {{
        background: rgba(14, 17, 23, 0.7) !important; /* Semi-transparan */
        backdrop-filter: blur(2px); /* Efek blur opsional */
        border-radius: 10px;
    }}
    /* Sidebar: Set semi-transparan */
    [data-testid="stSidebar"] {{
        background: rgba(14, 17, 23, 0.9) !important; 
    }}
    
    /* 4. DEFINISI KEYFRAMES UNTUK ANIMASI */
    @keyframes image-swap {{
        /* Gambar 1 */
        0%      {{ background-image: url('{IMG_URLS[0]}'); }}
        20%     {{ background-image: url('{IMG_URLS[0]}'); }}
        
        /* Transisi ke Gambar 2 */
        24%     {{ opacity: 0.2; }}
        25%     {{ background-image: url('{IMG_URLS[1]}'); opacity: 0.5; }}

        /* Gambar 2 */
        45%     {{ background-image: url('{IMG_URLS[1]}'); }}
        
        /* Transisi ke Gambar 3 (GIF) */
        49%     {{ opacity: 0.2; }}
        50%     {{ background-image: url('{IMG_URLS[2]}'); opacity: 0.5; }}

        /* Gambar 3 (GIF) */
        70%     {{ background-image: url('{IMG_URLS[2]}'); }}

        /* Transisi ke Gambar 4 */
        74%     {{ opacity: 0.2; }}
        75%     {{ background-image: url('{IMG_URLS[3]}'); opacity: 0.5; }}

        /* Gambar 4 */
        95%     {{ background-image: url('{IMG_URLS[3]}'); }}
        
        /* Transisi kembali ke Gambar 1 */
        99%     {{ opacity: 0.2; }}
        100%    {{ background-image: url('{IMG_URLS[0]}'); opacity: 0.5; }}
    }}
    </style>
    """
    st.markdown(css_animation, unsafe_allow_html=True)

# Panggil fungsi CSS sebelum konfigurasi Streamlit
set_animated_background()

# ==========================
# Load Models (basecode)
# ==========================
@st.cache_resource
def load_models():
    try:
        yolo_model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")  # Model deteksi objek
        classifier = tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")  # Model klasifikasi
        return yolo_model, classifier
    except Exception as e:
        return None, None, str(e)

# Load model dan tangani error
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
# Halaman HOME (Sudah Diperbaiki)
# ==========================
if st.session_state.page == "home":
    # Judul dan pengantar 
    st.markdown("<h1 style='text-align:center; color:#FF4B4B; text-shadow: 2px 2px 4px #000000;'>🔥 Aplikasi Analisis Kebakaran Hutan</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 18px; color: white; text-shadow: 1px 1px 3px #000000;'>Pilih salah satu layanan analitik di bawah untuk memulai pemrosesan gambar Anda.</p>", unsafe_allow_html=True)
    
    st.markdown("---") 

    col_classify, col_detect = st.columns(2)

    # --- Kartu Klasifikasi ---
    with col_classify:
        with st.container(border=True): 
            st.header("🖼 Klasifikasi Gambar") 
            st.caption("Cek Tipe Gambar")
            st.write("Sistem akan mengklasifikasikan gambar yang Anda unggah sebagai **'Kebakaran Hutan'** atau **'Bukan Kebakaran Hutan'**.")
            st.button("➡️ Mulai Klasifikasi", key="home_open_classify_unique",
                      on_click=go_to, args=("classify",), use_container_width=True, type="primary")

    # --- Kartu Deteksi Objek ---
    with col_detect:
        with st.container(border=True):
            st.header("🎯 Deteksi Objek") 
            st.caption("Temukan Lokasi Spesifik")
            st.write("Sistem akan mendeteksi dan menandai **api** atau **asap** di dalam gambar, memberikan *bounding box* hasil deteksi.")
            st.button("➡️ Mulai Deteksi Objek", key="home_open_detect_unique",
                      on_click=go_to, args=("detect",), use_container_width=True, type="primary")

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True) 

# ==========================
# Halaman KLASIFIKASI GAMBAR
# ==========================
elif st.session_state.page == "classify":
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
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = img_array / 255.0

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
# Halaman DETEKSI OBJEK
# ==========================
elif st.session_state.page == "detect":
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
