import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

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
                cursor:pointer;
            " onclick="window.location.href='?page=classify'">
                KLASIFIKASI GAMBAR
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tombol cadangan untuk Streamlit event (agar interaktif juga di rerun)
        if st.button("➡️ Buka Klasifikasi Gambar", key="to_classify"):
            go_to("classify")

    # Kotak Biru - menuju deteksi objek
    with col2:
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
                cursor:pointer;
            " onclick="window.location.href='?page=detect'">
                DETEKSI OBJEK
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tombol cadangan
        if st.button("➡️ Buka Deteksi Objek", key="to_detect"):
            go_to("detect")

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
