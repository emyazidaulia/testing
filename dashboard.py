import streamlit as st
import base64
import os

# --- Fungsi untuk encode gambar lokal ke base64 ---
def load_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- Fungsi untuk background slideshow (fade in–fade out) ---
def set_slideshow_background_local(image_paths, duration=18):
    base64_images = [f"data:image/jpeg;base64,{load_image_as_base64(img)}" for img in image_paths]
    total = len(base64_images)
    css_images = ""

    for i, url in enumerate(base64_images):
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
        background: rgba(0,0,0,0.4);
        z-index: 1;
    }}

    {css_images}
    </style>

    <div class="bg-slideshow">
        {''.join('<div class="bg-slide"></div>' for _ in base64_images)}
    </div>
    """, unsafe_allow_html=True)

# --- Contoh penggunaan ---
image_folder = "sample_images"
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
set_slideshow_background_local(image_files, duration=20)
