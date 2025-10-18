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

    # Kotak Merah → Klasifikasi
    with col1:
        st.markdown(
            """
            <div style='
                height:300px;
                background-color:#ff4b4b;
                border-radius:25px;
