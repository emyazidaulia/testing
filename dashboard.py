import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    # Logika navigasi sederhana, tidak perlu double click
    st.session_state.page = page_name

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    
    # Tambahkan key spesifik pada tombol Sidebar
    if st.button("🏠 Home", key="sidebar_home"):
        go_to("home")
    if st.button("🖼 Klasifikasi Gambar", key="sidebar_classify"):
        go_to("classify")
    if st.button("🎯 Deteksi Objek", key="sidebar_detect"):
        go_to("detect")

# --- Halaman HOME ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        
        # Tambahkan key spesifik pada tombol di Halaman Home
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True, key="home_classify"):
            go_to("classify")
            
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True, key="home_detect"):
            go_to("detect")

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini (gunakan model.h5 kamu).")

    # Tambahkan key spesifik
    if st.button("⬅ Kembali ke Home", key="classify_back"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini (gunakan model YOLO, dll).")

    # Tambahkan key spesifik
    if st.button("⬅ Kembali ke Home", key="detect_back"):
        go_to("home")
