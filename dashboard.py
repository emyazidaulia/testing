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
    # --- CSS Trik untuk Mengubah Background Halaman Utama saat Tombol di-Hover ---
    # Kita menggunakan `data-testid` dari Streamlit untuk menargetkan elemen.
    # [data-testid="stAppViewContainer"] adalah wrapper untuk seluruh aplikasi.
    # [data-testid="stKey_classify_btn"] adalah tombol Klasifikasi.
    st.markdown("""
    <style>
    /* Default Background (warna atau gambar default halaman) */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f0f2f6; /* Warna default Streamlit light mode */
        transition: background-image 0.5s ease, background-color 0.5s ease;
    }
    
    /* Menambahkan ID unik untuk tombol Klasifikasi */
    /* Kita gunakan key="classify_btn_home" agar selector lebih spesifik */
    
    /* Targetkan Tombol Klasifikasi */
    /* stKey_classify_btn_home adalah div wrapper tombol */
    
    /* Trik: Ketika tombol di-hover, coba ubah background elemen utama (stAppViewContainer) */
    /* Catatan: Ini SANGAT bergantung pada struktur DOM Streamlit dan mungkin TIDAK BEKERJA */
    div[data-testid="stKey_classify_btn_home"] button:hover {
        /* Properti tombol saat di-hover */
        transform: scale(1.05);
    }

    /* Trik paling stabil: Gunakan CSS untuk mengubah background DIV di dalam Main Container */
    /* Kita akan mengubah background DIV yang mengelilingi tombol saat tombol di-hover. */
    
    /* Karena perubahan background seluruh halaman sangat sulit,
       kita akan memodifikasi *background* tombol itu sendiri agar terlihat seperti kebakaran hutan
       DAN menambahkan border/shadow yang dramatis untuk efek yang kuat. */
       
    .stButton button {
        /* Gaya tombol agar kontras dengan background gelap */
        color: white;
        background-color: #764ba2;
        border: none;
        height: 80px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    /* Targetkan tombol Klasifikasi dengan key yang spesifik */
    div[data-testid="stKey_classify_btn_home"] button:hover {
        background-color: #ff4b4b !important; /* Warna merah api saat di-hover */
        box-shadow: 0 0 20px 5px rgba(255, 69, 0, 0.8) !important; /* Efek menyala */
        
        /* Trik untuk menambahkan background image di dalam tombol (jika mendukung) */
        background-image: url('https://images.unsplash.com/photo-1542382109289-4a0b27192f16?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
    }

    </style>
    """, unsafe_allow_html=True)
    
    # --- Konten Halaman HOME ---
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        
        # Tambahkan key spesifik untuk tombol Klasifikasi
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True, key="classify_btn_home"):
            go_to("classify")
            
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
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
