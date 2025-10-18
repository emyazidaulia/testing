import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image App", layout="wide")

# --- Inisialisasi session state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name


# =====================================================
#                     HALAMAN HOME
# =====================================================
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)

    # CSS styling
    st.markdown("""
        <style>
        .full-box {
            height: 450px;
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
            text-align: center;
        }
        .full-box:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 30px rgba(0,0,0,0.25);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # Kotak merah
    with col1:
        box1 = st.container()
        with box1:
            if st.button(" ", key="goto_classify", use_container_width=True):
                go_to("classify")
            st.markdown(
                """
                <div class="full-box" style="background-color:#ff4b4b; margin-top:-90px;">
                    KLASIFIKASI GABAR
                </div>
                """,
                unsafe_allow_html=True
            )

    # Kotak biru
    with col2:
        box2 = st.container()
        with box2:
            if st.button(" ", key="goto_detect", use_container_width=True):
                go_to("detect")
            st.markdown(
                """
                <div class="full-box" style="background-color:#4287f5; margin-top:-90px;">
                    DETEKSI OBJEK
                </div>
                """,
                unsafe_allow_html=True
            )


# =====================================================
#              HALAMAN KLASIFIKASI GAMBAR
# =====================================================
elif st.session_state.page == "classify":
    st.header("🖼️ Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi siap dijalankan (gunakan model.h5 kamu).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))

# =====================================================
#                HALAMAN DETEKSI OBJEK
# =====================================================
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi siap dijalankan (gunakan model YOLO, dll).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))
