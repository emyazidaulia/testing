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
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
        }
        .big-box:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 30px rgba(0,0,0,0.25);
        }
        </style>
    """, unsafe_allow_html=True)

    # Kotak merah (klik → klasifikasi)
    with col1:
        if st.markdown(
            """<div class="big-box" style="background-color:#ff4b4b;" onclick="window.parent.postMessage({func:'go_classify'}, '*')">KLASIFIKASI GAMBAR</div>""",
            unsafe_allow_html=True
        ):
            pass  # Kosong karena klik akan ditangani oleh JS

    # Kotak biru (klik → deteksi)
    with col2:
        if st.markdown(
            """<div class="big-box" style="background-color:#4287f5;" onclick="window.parent.postMessage({func:'go_detect'}, '*')">DETEKSI OBJEK</div>""",
            unsafe_allow_html=True
        ):
            pass

    # Tangkap postMessage dari JS
    st.components.v1.html("""
        <script>
        window.addEventListener('message', (event) => {
            if(event.data.func == 'go_classify'){
                window.location.reload();  // reload agar Streamlit tangkap state baru
            } else if(event.data.func == 'go_detect'){
                window.location.reload();
            }
        });
        </script>
    """, height=0)
