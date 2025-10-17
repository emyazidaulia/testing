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

# --- Halaman HOME ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # CSS custom: buat div bisa klik + animasi hover
    st.markdown("""
        <style>
        .clickable-box {
            height: 400px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
            font-weight: bold;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .clickable-box:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 25px rgba(0,0,0,0.3);
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Kotak Merah
    with col1:
        if st.button(" ", key="red_box", use_container_width=True):
            go_to("classify")

        st.markdown(
            """
            <div class="clickable-box" 
                 style="background-color:#ff4b4b; margin-top:-70px;"
                 onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'red_box', value: true}, '*')">
                KLASIFIKASI GAMBAR
            </div>
            """,
            unsafe_allow_html=True
        )

    # Kotak Biru
    with col2:
        if st.button(" ", key="blue_box", use_container_width=True):
            go_to("detect")

        st.markdown(
            """
            <div class="clickable-box"
                 style="background-color:#4287f5; margin-top:-70px;"
                 onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'blue_box', value: true}, '*')">
                DETEKSI OBJEK
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.header("🖼️ Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi siap dijalankan di sini (gunakan model.h5 kamu).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi siap dijalankan di sini (gunakan model YOLO, dll).")

    st.button("⬅️ Kembali ke Home", on_click=lambda: go_to("home"))
