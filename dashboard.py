import streamlit as st

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

    # Menambahkan CSS untuk efek hover pada *wrapper* tombol (SOLUSI STABIL)
    st.markdown("""
    <style>
    /* -------------------------------------------------------------------------- */
    /* Gaya Umum Tombol */
    /* -------------------------------------------------------------------------- */
    .stButton > button {
        height: 80px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: white; /* Pastikan teks terlihat di dark mode */
        background-color: #764ba2; /* Warna default tombol */
    }
    .stButton > button:hover {
        transform: scale(1.03);
    }
    
    /* -------------------------------------------------------------------------- */
    /* Gaya untuk Wrapper Tombol Klasifikasi */
    /* -------------------------------------------------------------------------- */
    /* Target div wrapper tombol menggunakan data-testid dari key="classify_btn_home" */
    
    div[data-testid="stKey_classify_btn_home"] {
        position: relative;
        overflow: hidden; /* Penting untuk mengontrol ::before */
        border-radius: 10px; /* Cocokkan dengan tombol */
        transition: all 0.3s ease;
        background-color: transparent; /* Pastikan tombol di dalamnya yang mendefinisikan warna */
        padding: 5px; /* Tambahkan sedikit padding agar efek ::before memiliki ruang */
    }

    /* Pseudo-element untuk background image saat hover */
    div[data-testid="stKey_classify_btn_home"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        /* GAMBAR KEBAKARAN HUTAN */
        background-image: url('https://images.unsplash.com/photo-1542382109289-4a0b27192f16?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0; /* Sembunyikan secara default */
        transition: opacity 0.5s ease;
        z-index: 0; /* Letakkan di bawah tombol */
        border-radius: 10px;
    }

    /* Efek hover: Tampilkan background image */
    div[data-testid="stKey_classify_btn_home"]:hover::before {
        opacity: 0.6; /* Tampilkan dengan opacity 60% */
    }

    /* Pastikan tombol dan teksnya berada di atas background image */
    div[data-testid="stKey_classify_btn_home"] button {
        position: relative;
        z-index: 1; /* Pastikan di atas ::before */
        background-color: rgba(118, 75, 162, 0.7) !important; /* Buat tombol agak transparan agar gambar terlihat */
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.5); /* Tambahkan shadow api */
    }

    /* Hapus padding div wrapper Streamlit yang tidak perlu */
    [data-testid="stKey_classify_btn_home"] > div {
        padding: 0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        
        # Tombol Klasifikasi dengan key spesifik untuk CSS
        # Penting: Tombol harus berada di dalam wrapper div agar ::before berfungsi
        if st.button("🔥 Buka Klasifikasi Gambar", use_container_width=True, key="classify_btn_home"):
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
