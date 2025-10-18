import streamlit as st
import base64
from pathlib import Path

# --- Fungsi Konversi Gambar Lokal ke Base64 ---
def get_base64_image(image_path):
    """Mengonversi file gambar lokal ke Base64 string."""
    try:
        # Path relatif ke folder sample_images
        img_path = Path(image_path)
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: File gambar tidak ditemukan di {image_path}. Pastikan path sudah benar.")
        return "" # Mengembalikan string kosong jika gagal

# Definisikan path gambar lokal untuk hover (misal: abc016.jpg)
IMAGE_PATH = "sample_images/abc016.jpg" 
base64_image = get_base64_image(IMAGE_PATH)

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

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
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # --- CSS Trik untuk Efek Hover dengan Gambar Base64 ---
    if base64_image:
        FIRE_IMAGE_CSS = f"""
        <style>
        /* -------------------------------------------------------------------------- */
        /* Gaya Umum Tombol */
        /* -------------------------------------------------------------------------- */
        .stButton > button {{
            height: 80px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            color: white; /* Pastikan teks terlihat di dark mode */
            background-color: #764ba2; /* Warna default tombol */
        }}
        .stButton > button:hover {{
            transform: scale(1.03);
        }}
        
        /* -------------------------------------------------------------------------- */
        /* Gaya untuk Wrapper Tombol Klasifikasi (Menggunakan Gambar Lokal) */
        /* -------------------------------------------------------------------------- */
        /* Target div wrapper tombol menggunakan data-testid dari key="classify_btn_home" */
        
        div[data-testid="stKey_classify_btn_home"] {{
            position: relative;
            overflow: hidden; 
            border-radius: 10px; 
            transition: all 0.3s ease;
            background-color: transparent; 
            padding: 5px;
        }}

        /* Pseudo-element untuk background image saat hover */
        div[data-testid="stKey_classify_btn_home"]::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            /* GAMBAR LOKAL ABC016.JPG YANG SUDAH DI-BASE64 */
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            opacity: 0; /* Sembunyikan secara default */
            transition: opacity 0.5s ease;
            z-index: 0; /* Letakkan di bawah tombol */
            border-radius: 10px;
        }}

        /* Efek hover: Tampilkan background image */
        div[data-testid="stKey_classify_btn_home"]:hover::before {{
            opacity: 0.6; /* Tampilkan dengan opacity 60% */
        }}

        /* Pastikan tombol dan teksnya berada di atas background image */
        div[data-testid="stKey_classify_btn_home"] button {{
            position: relative;
            z-index: 1; /* Pastikan di atas ::before */
            background-color: rgba(118, 75, 162, 0.7) !important; /* Buat tombol agak transparan agar gambar terlihat */
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.5); /* Tambahkan shadow api */
        }}

        /* Hapus padding div wrapper Streamlit yang tidak perlu */
        [data-testid="stKey_classify_btn_home"] > div {{
            padding: 0 !important;
        }}
        
        </style>
        """
        st.markdown(FIRE_IMAGE_CSS, unsafe_allow_html=True)
    else:
        st.warning("Gagal memuat gambar lokal. Efek hover mungkin tidak berfungsi.")


    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        
        # Tombol Klasifikasi dengan key spesifik untuk CSS
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True, key="classify_btn_home"):
            go_to("classify")
            
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        
        # Tombol Deteksi (tanpa efek khusus)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True):
            go_to("detect")

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")
