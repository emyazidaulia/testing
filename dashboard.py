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
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ------------------ Kotak Merah ------------------
    with col1:
        container_red = st.container()
        with container_red:
            # Kotak visual
            st.markdown('''
                <div style="
                    height:300px;
                    background-color:#ff4b4b;
                    border-radius:25px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:28px;
                    font-weight:bold;
                    transition: all 0.25s ease;
                " onmouseover="">
                    KLASIFIKASI GAMBAR
                </div>
            ''', unsafe_allow_html=True)
            # Tombol overlay transparan agar klik di mana saja di kotak
            if st.button(" ", key="classify_overlay", use_container_width=True):
                go_to("classify")

    # ------------------ Kotak Biru ------------------
    with col2:
        container_blue = st.container()
        with container_blue:
            st.markdown('''
                <div style="
                    height:300px;
                    background-color:#4287f5;
                    border-radius:25px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:28px;
                    font-weight:bold;
                    transition: all 0.25s ease;
                ">
                    DETEKSI OBJEK
                </div>
            ''', unsafe_allow_html=True)
            if st.button(" ", key="detect_overlay", use_container_width=True):
                go_to("detect")

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
