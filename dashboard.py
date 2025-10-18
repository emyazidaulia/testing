import streamlit as st

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

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
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # Menambahkan CSS untuk efek hover dengan gambar background
    st.markdown("""
    <style>
    /* Container untuk tombol klasifikasi dengan efek hover */
    .classify-container {
        position: relative;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .classify-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
    }
    
    .classify-container:hover::before {
        opacity: 0.3;
    }
    
    .classify-container > * {
        position: relative;
        z-index: 2;
    }
    
    /* Container untuk tombol deteksi dengan efek hover */
    .detect-container {
        position: relative;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .detect-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
    }
    
    .detect-container:hover::before {
        opacity: 0.3;
    }
    
    .detect-container > * {
        position: relative;
        z-index: 2;
    }
    
    /* Style untuk tombol */
    .stButton > button {
        height: 80px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Layout tombol di tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
        
        # Container untuk tombol klasifikasi dengan efek hover
        st.markdown('<div class="classify-container">', unsafe_allow_html=True)
        if st.button("🖼 Buka Klasifikasi Gambar", use_container_width=True, key="classify_btn"):
            go_to("classify")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        
        # Container untuk tombol deteksi dengan efek hover
        st.markdown('<div class="detect-container">', unsafe_allow_html=True)
        if st.button("🎯 Buka Deteksi Objek", use_container_width=True, key="detect_btn"):
            go_to("detect")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Halaman KLASIFIKASI GAMBAR ---
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")
    uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model klasifikasi dapat dijalankan di sini (gunakan model.h5 kamu).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")

# --- Halaman DETEKSI OBJEK ---
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")
    uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
        st.success("Model deteksi dapat dijalankan di sini (gunakan model YOLO, dll).")

    if st.button("⬅ Kembali ke Home"):
        go_to("home")
