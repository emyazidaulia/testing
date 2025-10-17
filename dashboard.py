import streamlit as st
import time

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if "fade" not in st.session_state:
    st.session_state.fade = True  # untuk trigger animasi

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.fade = False  # untuk fade-out sebelum pindah halaman
    st.experimental_rerun()
    time.sleep(0.2)
    st.session_state.page = page_name
    st.session_state.fade = True

# --- CSS Animasi (fade in/out) ---
fade_css = """
<style>
.fade-in {
  animation: fadeIn 0.8s ease-in-out;
}
.fade-out {
  animation: fadeOut 0.5s ease-in-out;
}
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
@keyframes fadeOut {
  from {opacity: 1;}
  to {opacity: 0;}
}
</style>
"""

st.markdown(fade_css, unsafe_allow_html=True)
animation_class = "fade-in" if st.session_state.fade else "fade-out"

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.session_state.fade = True
        st.experimental_rerun()
    if st.button("🖼️ Klasifikasi Gambar"):
        st.session_state.page = "classify"
        st.session_state.fade = True
        st.experimental_rerun()
    if st.button("🎯 Deteksi Objek"):
        st.session_state.page = "detect"
        st.session_state.fade = True
        st.experimental_rerun()

# ============================
#         HALAMAN HOME
# ============================
if st.session_state.page == "home":
    st.markdown(f"<div class='{animation_class}'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # Tombol tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        if st.button("🖼️ Buka Klasifikasi Gambar", use_container_width=True):
            st.session_state.page = "classify"
            st.session_state.fade = True
            st.experimental_rerun()
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True):
            st.session_state.page = "detect"
            st.session_state.fade = True
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================
#     HALAMAN KLASIFIKASI
# ============================
elif st.session_state.page == "classify":
    st.markdown(f"<div class='{animation_class}'>", unsafe_allow_html=True)
    st.header("🖼️ Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅️ Kembali ke Home"):
        st.session_state.page = "home"
        st.session_state.fade = True
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
#      HALAMAN DETEKSI
# ============================
elif st.session_state.page == "detect":
    st.markdown(f"<div class='{animation_class}'>", unsafe_allow_html=True)
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅️ Kembali ke Home"):
        st.session_state.page = "home"
        st.session_state.fade = True
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
