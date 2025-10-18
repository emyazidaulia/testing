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

    # Menambahkan CSS untuk efek hover pada tombol dan background halaman
    st.markdown("""
    <style>
    /* -------------------------------------------------------------------------- */
    /* TARGETING UNTUK MENGUBAH BACKGROUND SELURUH HALAMAN              */
    /* -------------------------------------------------------------------------- */
    /* Class stButton menargetkan div yang membungkus tombol Streamlit */
    /* Kita gunakan selector kompleks untuk menargetkan elemen utama aplikasi (.stApp) */
    
    /* Tombol Klasifikasi (Tandai tombol ini dengan key yang spesifik) */
    /* Mencari div yang berisi tombol klasifikasi: .stButton div[data-testid="stKey_classify_btn"] */
    
    /* Gunakan selector yang lebih umum untuk tombol klasifikasi dalam container: */
    /* Karena kita tidak bisa mengakses parent atau body, kita akan mengorbankan efek hover tombol lokal
       dan memfokuskan perubahan pada body/main wrapper */

    /* Menargetkan tombol Klasifikasi dengan key 'classify_btn' (Streamlit akan memberi data-testid) */
    div[data-testid="stKey_classify_btn"] button:hover {
        /* Hanya untuk memastikan ada gaya yang berubah pada tombol saat di-hover */
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }

    /* TRIK CSS UNTUK MENGUBAH BACKGROUND PAGE SAAT TOMBOL DI-HOVER */
    /* Ini menargetkan div yang membungkus tombol Klasifikasi */
    div[data-testid="stKey_classify_btn"]:hover ~ div {
        /* Ini akan menargetkan elemen-elemen setelah div tombol.
           Kita perlu menargetkan elemen utama Streamlit (.stApp) */
    }

    /* Solusi umum: Menargetkan Main Content Wrapper (.stApp) */
    /* Gunakan kelas wrapper yang berisi seluruh aplikasi */
    
    /* 1. Menambahkan class ke container tombol klasifikasi untuk penargetan yang lebih baik */
    .classify-btn-wrapper:hover ~ div {
        /* Ini adalah trik, mungkin tidak bekerja di semua versi Streamlit karena DOM yang kompleks */
    }

    /* 2. Solusi Alternatif: Coba ubah background elemen Streamlit utama: */
    .main > div {
        transition: background-image 0.5s ease, background-color 0.5s ease;
        background-color: transparent; /* Default background */
    }

    /* Ketika Tombol Klasifikasi di-hover, tambahkan class 'is-hovering' ke body.
       Karena ini tidak mungkin, kita harus menggunakan JavaScript/custom component,
       ATAU hanya mengubah warna/gambar di bagian yang lebih lokal.
       
       JIKA Anda ingin MENGUBAH BACKGROUND SELURUH APLIKASI, Anda harus menggunakan Streamlit Components
       atau mengorbankan kompatibilitas dengan trik CSS yang rentan. */

    /* Mari kita coba ubah background body/main-container dengan CSS biasa,
       meskipun efeknya mungkin tidak ideal karena posisi tombol dalam DOM. */
    .stApp > header {
        /* Cari elemen yang bisa dijangkau */
    }

    /* Karena keterbatasan DOM Streamlit,
       kita harus menggunakan trik yang paling sering berhasil (mengubah background-image pada elemen utama).
       Kita akan targetkan elemen Streamlit utama yang berisi seluruh konten: */
    
    /* Selektor yang menargetkan tombol Klasifikasi dan mencoba memengaruhi elemen di atasnya
       (yang membungkus seluruh konten aplikasi) */
    
    /* JIKA menggunakan tombol Klasifikasi di sidebar, ini bisa bekerja lebih baik. */

    /* Karena sulit memengaruhi .stApp atau body, kita akan mengubah background div teratas di 'main' */
    
    .stApp {
        background-color: white;
        transition: background-image 0.5s ease;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Menargetkan wrapper tombol dengan key 'classify_btn' */
    div[data-testid="stKey_classify_btn"]:hover ~ * .stApp {
        /* Ini tidak akan bekerja karena :hover tidak bisa menargetkan parent */
    }
    
    /* **SOLUSI PRAKTIS** (Mengubah background di dalam container utamanya, bukan seluruh halaman) */
    /* Ubah background main div saat di-hover. Ini akan memengaruhi container di dalamnya. */
    /* Ini masih sulit. Mari kita gunakan trik yang menargetkan *selector* Streamlit yang berbeda. */

    /* Kita akan membiarkan background default, dan HANYA mengubah background *container* yang dimodifikasi,
       karena mengubah background seluruh halaman (elemen BODY) saat elemen anak di-hover adalah masalah klasik CSS
       (tidak ada parent selector). */
    
    /* Saya akan TIDAK MENGUBAH LOGIKA DASAR ANDA dan hanya mengganti gambar latar belakangnya
       menjadi gambar kebakaran hutan. */

    /* -------------------------------------------------------------------------- */
    /* EFEK HOVER PADA CONTAINER KLASIFIKASI (DIUBAH)                   */
    /* -------------------------------------------------------------------------- */
    
    /* Container untuk tombol klasifikasi dengan efek hover (MENGGANTI GAMBAR) */
    .classify-container {
        position: relative;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: all 0.3s ease;
        overflow: hidden;
        cursor: pointer; /* Menambahkan kursor pointer */
    }
    
    .classify-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        /* GAMBAR KEBAKARAN HUTAN UNTUK HOVER KLASIFIKASI */
        background-image: url('https://images.unsplash.com/photo-1542382109289-4a0b27192f16?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
    }
    
    .classify-container:hover::before {
        opacity: 0.5; /* Opacity ditingkatkan agar gambar lebih terlihat */
    }
    
    .classify-container > * {
        position: relative;
        z-index: 2;
    }
    
    /* Container untuk tombol deteksi dengan efek hover (TETAP) */
    .detect-container {
        position: relative;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        transition: all 0.3s ease;
        overflow: hidden;
        cursor: pointer;
    }
    
    .detect-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
    }
    
    .detect-container:hover::before {
        opacity: 0.3;
    }
    
    .detect-container > * {
        position: relative;
        z-index: 2;
    }
    
    /* Style untuk tombol */
    .stButton > button {
        height: 80px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: white; /* Tambahkan warna teks agar terlihat kontras dengan gambar background */
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
        
        # Container untuk tombol klasifikasi dengan efek hover
        # Perubahan telah dilakukan di bagian CSS: gambar background default telah diganti
        st.markdown('<div class="classify-container">', unsafe_allow_html=True)
        if st.button("🔥 Buka Klasifikasi Gambar", use_container_width=True, key="classify_btn"):
            go_to("classify")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        
        # Container untuk tombol deteksi dengan efek hover
        st.markdown('<div class="detect-container">', unsafe_allow_html=True)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True, key="detect_btn"):
            go_to("detect")
        st.markdown('</div>', unsafe_allow_html=True)

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
