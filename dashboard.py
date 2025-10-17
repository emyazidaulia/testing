import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi halaman ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi untuk berpindah halaman ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Fungsi background slideshow (fade in–fade out) ---
def set_slideshow_background(image_urls, duration=18):
    total = len(image_urls)
    css_images = ""
    for i, url in enumerate(image_urls):
        delay = (i * (duration / total))
        css_images += f"""
        .bg-slide:nth-child({i+1}) {{
            background-image: url('{url}');
            animation-delay: {delay}s;
        }}
        """

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        position: relative;
        overflow: hidden;
        background: black;
    }}

    .bg-slideshow {{
        position: fixed;
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

    .bg-slideshow::after {{
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.4); /* agar teks lebih terbaca */
        z-index: 1;
    }}

    {css_images}
    </style>

    <div class="bg-slideshow">
        {''.join('<div class="bg-slide"></div>' for _ in image_urls)}
    </div>
    """, unsafe_allow_html=True)

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
    # Ganti URL sesuai repo GitHub kamu (gunakan "raw.githubusercontent.com")
    set_slideshow_background([
        "https://raw.githubusercontent.com/username/repo/main/sample_images/00000055.jpg",
        "https://raw.githubusercontent.com/username/repo/main/sample_images/00000076.jpg",
        "https://raw.githubusercontent.com/username/repo/main/sample_images/abc016.jpg",
        "https://raw.githubusercontent.com/username/repo/main/sample_images/abc018.jpg"
    ], duration=20)

    st.markdown("<h1 style='text-align:center;color:white;'>Selamat Datang di Aplikasi!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:white;'>Pilih menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        if st.button("🖼 Menu Klasifikasi Gambar", use_container_width=True):
            go_to("classify")
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Menu Deteksi Objek", use_container_width=True):
            go_to("detect")

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    set_slideshow_background([
        "https://raw.githubusercontent.com/username/repo/main/sample_images/abc017.jpg",
        "https://raw.githubusercontent.com/username/repo/main/sample_images/abc018.jpg"
    ], duration=16)

    st.header("🖼 Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini.")
    if st.button("⬅ Kembali ke Home"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    set_slideshow_background([
        "https://raw.githubusercontent.com/username/repo/main/sample_images/00000078.jpg",
        "https://raw.githubusercontent.com/username/repo/main/sample_images/abc016.jpg"
    ], duration=16)

    st.header("🎯 Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini.")
    if st.button("⬅ Kembali ke Home"):
        go_to("home")
