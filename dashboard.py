import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================

# DAFTAR NAMA KELAS
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan'] 

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
        st.error(f"Gagal memuat model. Pastikan file model ada di direktori 'model/'. Error: {e}")
        return None, None

yolo_model, classifier = load_models()

# --- CSS untuk Animasi Fade In ---
st.markdown("""
<style>
/* Definisikan keyframes untuk fade-in */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Terapkan animasi ke konten utama */
.content-fade-in {
    animation: fadeIn 0.6s ease-out; /* Durasi 0.6 detik */
}

/* Sembunyikan tombol navigasi Streamlit yang tidak digunakan */
.stButton>button {
    /* Menjaga tombol tetap terlihat */
}
</style>
""", unsafe_allow_html=True)
# ----------------------------------

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier & Detection", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    if st.button("🏠 Home"):
        go_to("home")
    if st.button("🖼 Klasifikasi Gambar"):
        go_to("classify")
    if st.button("🎯 Deteksi Objek"):
        go_to("detect")

# --- Halaman HOME ---
if st.session_state.page == "home":
    # Pembungkus dengan class animasi
    st.markdown('<div class="content-fade-in">', unsafe_allow_html=True) 
    
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True):
            go_to("classify")
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True):
            go_to("detect")
            
    st.markdown('</div>', unsafe_allow_html=True) # Penutup pembungkus

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    # Pembungkus dengan class animasi
    st.markdown('<div class="content-fade-in">', unsafe_allow_html=True)
    
    st.header("🖼 Menu Klasifikasi Gambar")
    
    if classifier is None:
        st.warning("Model Klasifikasi tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            # Preprocessing dan prediksi
            with st.spinner('Memproses Klasifikasi...'):
                img_resized = img.resize((128, 128)) 
                img_array = image.img_to_array(img_resized)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                prediction = classifier.predict(img_array)
                class_index = np.argmax(prediction)
                probability = np.max(prediction)
                
                # Menampilkan NAMA KELAS 
                if class_index < len(CLASS_NAMES):
                    predicted_class = CLASS_NAMES[class_index]
                    st.success("✅ Klasifikasi Selesai!")
                    st.markdown(f"### Hasil Prediksi: **{predicted_class}**")
                    st.write(f"**Probabilitas:** {probability*100:.2f}%")
                else:
                    st.error("Indeks kelas tidak valid. Pastikan CLASS_NAMES sudah benar.")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")
        
    st.markdown('</div>', unsafe_allow_html=True) # Penutup pembungkus

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    # Pembungkus dengan class animasi
    st.markdown('<div class="content-fade-in">', unsafe_allow_html=True)
    
    st.header("🎯 Menu Deteksi Objek")

    if yolo_model is None:
        st.warning("Model Deteksi Objek tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            # Deteksi objek
            with st.spinner('Memproses Deteksi Objek...'):
                results = yolo_model(img)
                result_img = results[0].plot()
                
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
                st.success("✅ Deteksi Selesai!")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")
        
    st.markdown('</div>', unsafe_allow_html=True) # Penutup pembungkus
