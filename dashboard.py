import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Fungsi untuk background slideshow (fade in/out) ---
def set_slideshow_background(image_paths, duration=10):
    """
    Menampilkan background slideshow dari beberapa gambar lokal.
    - image_paths: list path gambar lokal
    - duration: waktu total 1 siklus (detik)
    """
    images_css = ""
    total = len(image_paths)
    for i, img in enumerate(image_paths):
        delay = (i * (duration / total))
        images_css += f"""
        .bg-slide:nth-child({i+1}) {{
            background-image: url("{img}");
            animation-delay: {delay}s;
        }}
        """

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            position: relative;
            overflow: hidden;
        }}

        .bg-slideshow {{
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}

        .bg-slide {{
            position: absolute;
            width: 100%;
            height: 100%;
            background-size: cover;
            background-position: center;
            opacity: 0;
            animation: fadeinout {duration}s infinite;
        }}

        @keyframes fadeinout {{
            0%, 100% {{ opacity: 0; }}
            10%, 45% {{ opacity: 1; }}
        }}

        {images_css}
        </style>

        <div class="bg-slideshow">
            {''.join('<div class="bg-slide"></div>' for _ in image_paths)}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    if st.button("🏠 Home"):
        go_to("home")
    if st.button("🖼 Klasifikasi Gambar"):
        go_to("classify")
    if st.button("🎯 Deteksi Objek"):
        go_to("detect")

# --- Halaman HOME ---
if st.session_state.page == "home":
    set_slideshow_background(
        [
            "images/bg1.jpg",
            "images/bg2.jpg",
            "images/bg3.jpg",
        ],
        duration=15  # total durasi 15 detik per siklus
    )

    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True):
            go_to("classify")
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True):
            go_to("detect")

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    set_slideshow_background(
        [
            "images/class1.jpg",
            "images/class2.jpg",
            "images/class3.jpg",
        ],
        duration=12
    )

    st.header("🖼 Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    set_slideshow_background(
        [
            "images/detect1.jpg",
            "images/detect2.jpg",
            "images/detect3.jpg",
        ],
        duration=14
    )

    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")
