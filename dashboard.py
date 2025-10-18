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
        st.markdown('''
            <div style="
                height:300px;
                background-color:#ff4b4b;
                border-radius:25px;
                display:flex;
                align-items:center;
                justify-content:center;
                transition: all 0.25s ease;
                padding: 20px;
            ">
        ''', unsafe_allow_html=True)

        # Tombol interaktif di tengah kotak
        if st.button("Buka Klasifikasi", key="btn_classify", help="Klik untuk membuka menu klasifikasi gambar"):
            go_to("classify")

        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ Kotak Biru ------------------
    with col2:
        st.markdown('''
            <div style="
                height:300px;
                background-color:#4287f5;
                border-radius:25px;
                display:flex;
                align-items:center;
                justify-content:center;
                transition: all 0.25s ease;
                padding: 20px;
            ">
        ''', unsafe_allow_html=True)

        if st.button("Buka Deteksi Objek", key="btn_detect", help="Klik untuk membuka menu deteksi objek"):
            go_to("detect")

        st.markdown('</div>', unsafe_allow_html=True)

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
