import streamlit as st
import time

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

# --- CSS Animasi Fade ---
st.markdown("""
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    @keyframes fadeOut {
        from {opacity: 1;}
        to {opacity: 0;}
    }

    .fade-container {
        animation: fadeIn 0.7s ease-in-out;
        transition: opacity 0.5s ease-in-out;
    }

    .button-big {
        background-color: #2c2f33;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 25px 60px;
        font-size: 20px;
        cursor: pointer;
        transition: transform 0.2s ease, background-color 0.3s ease;
    }
    .button-big:hover {
        transform: scale(1.05);
        background-color: #4b5563;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    if st.button("🏠 Home"):
        go_to("home")
    if st.button("🖼️ Klasifikasi Gambar"):
        go_to("classify")
    if st.button("🎯 Deteksi Objek"):
        go_to("detect")

# --- Tampilan Halaman HOME ---
if st.session_state.page == "home":
    with st.container():
        st.markdown("<div class='fade-container'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🖼️ Buka Klasifikasi Gambar", use_container_width=True):
                go_to("classify")
            st.markdown(
                """
                <div style="
                    background-color:#ff4b4b;
                    height:400px;
                    border-radius:20px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:28px;
                    font-weight:bold;
                    margin-top:10px;
                ">
                    KLASIFIKASI GAMBAR
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            if st.button("🎯 Buka Deteksi Objek", use_container_width=True):
                go_to("detect")
            st.markdown(
                """
                <div style="
                    background-color:#4287f5;
                    height:400px;
                    border-radius:20px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:28px;
                    font-weight:bold;
                    margin-top:10px;
                ">
                    DETEKSI OBJEK
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.markdown("<div class='fade-container'>", unsafe_allow_html=True)
    st.header("🖼️ Menu Klasifikasi Gambar")

    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi bisa dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅️ Kembali ke Home"):
        go_to("home")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.markdown("<div class='fade-container'>", unsafe_allow_html=True)
    st.header("🎯 Menu Deteksi Objek")

    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi bisa dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅️ Kembali ke Home"):
        go_to("home")

    st.markdown("</div>", unsafe_allow_html=True)
