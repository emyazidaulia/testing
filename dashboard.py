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
    col1, col2 = st.columns(2)

    # CSS Styling untuk kotak besar
    st.markdown("""
        <style>
        .big-box {
            height: 400px;
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            transition: all 0.25s ease;
            position: relative;
        }
        .big-box:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 30px rgba(0,0,0,0.25);
        }
        </style>
    """, unsafe_allow_html=True)

    # Kotak merah
    with col1:
        if st.button(" ", key="goto_classify", help="Klik untuk membuka menu klasifikasi gambar", use_container_width=True):
            go_to("classify")

        st.markdown(
            """
            <div class="big-box" style="background-color:#ff4b4b; margin-top:-70px;">
                KLASIFIKASI GAMBAR
            </div>
            """,
            unsafe_allow_html=True
        )

    # Kotak biru
    with col2:
        if st.button(" ", key="goto_detect", help="Klik untuk membuka menu deteksi objek", use_container_width=True):
            go_to("detect")

        st.markdown(
            """
            <div class="big-box" style="background-color:#4287f5; margin-top:-70px;">
                DETEKSI OBJEK
            </div>
            """,
            unsafe_allow_html=True
        )

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
