import streamlit as st

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Image App", layout="wide")

# --- Inisialisasi session_state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi Navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🔍 Navigasi")
    st.button("🏠 Home", on_click=lambda: go_to("home"))
    st.button("🖼️ Klasifikasi Gambar", on_click=lambda: go_to("classify"))
    st.button("🎯 Deteksi Objek", on_click=lambda: go_to("detect"))

# =====================================================
#                     HALAMAN HOME
# =====================================================
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih menu di bawah untuk memulai.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    # ------------------ Kotak Merah ------------------
    with col1:
        # Tombol yang tampil seperti kotak besar
        if st.button("KLASIFIKASI GAMBAR", key="classify_btn", 
                     help="Klik untuk membuka menu klasifikasi gambar", 
                     use_container_width=True):
            go_to("classify")
        # Styling agar tombol terlihat seperti kotak besar
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                height: 300px;
                font-size: 28px;
                font-weight: bold;
                background-color: #ff4b4b;
                color: white;
                border-radius: 25px;
            }
            </style>
        """, unsafe_allow_html=True)

    # ------------------ Kotak Biru ------------------
    with col2:
        if st.button("DETEKSI OBJEK", key="detect_btn", 
                     help="Klik untuk membuka menu deteksi objek", 
                     use_container_width=True):
            go_to("detect")
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                height: 300px;
                font-size: 28px;
                font-weight: bold;
                background-color: #4287f5;
                color: white;
                border-radius: 25px;
            }
            </style>
        """, unsafe_allow_html=True)

# =====================================================
#            HALAMAN KLASIFIKASI GAMBAR
# =====================================================
elif st.session_state.page == "classify":
    st.header("🖼️ Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi siap dijalankan di sini (gunakan model.h5 kamu).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))

# =====================================================
#              HALAMAN DETEKSI OBJEK
# =====================================================
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi siap dijalankan di sini (gunakan model YOLO, dll).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))
