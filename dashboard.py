import streamlit as st

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi (tidak memanggil rerun eksplisit) ---
def go_to(page_name):
    st.session_state.page = page_name
    # tidak memanggil st.rerun() / st.experimental_rerun()

# --- Sidebar ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    if st.button("🏠 Home"):
        go_to("home")
    if st.button("🖼️ Klasifikasi Gambar"):
        go_to("classify")
    if st.button("🎯 Deteksi Objek"):
        go_to("detect")

# --- Tampilan halaman HOME ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Kotak Merah - menuju klasifikasi gambar
    with col1:
        # tombol transparan besar: capture klik seluruh area
        if st.button("🖼️ Buka Klasifikasi Gambar", key="to_classify", use_container_width=True):
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
            ">
                KLASIFIKASI GAMBAR
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Kotak Biru - menuju deteksi objek
    with col2:
        if st.button("🎯 Buka Deteksi Objek", key="to_detect", use_container_width=True):
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
            ">
                DETEKSI OBJEK
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.header("🖼️ Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi bisa dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅️ Kembali ke Home"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi bisa dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅️ Kembali ke Home"):
        go_to("home")
