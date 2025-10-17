# app.py
import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Pastikan file UTF-8 (biasanya default). Jika masih error, simpan file sebagai UTF-8.
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
    # Jangan panggil st.warning saat import time terlalu awal jika tidak ingin menulis ke UI saat import.
    YOLO_AVAILABLE = False
    YOLO_IMPORT_ERROR = str(e)

@st.cache_resource
def load_yolo_model():
    if YOLO_AVAILABLE:
        model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")
        model.overrides["save"] = False
        model.overrides["project"] = "/tmp"
        return model
    return None

@st.cache_resource
def load_classifier_model():
    return tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")

st.set_page_config(page_title="Would You Rather AI", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ====== HOME ======
if st.session_state.page == "home":
    st.markdown(
        """
        <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 3rem;
            height: 90vh;
        }
        .box {
            flex: 1;
            height: 70vh;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 25px;
            font-size: 2rem;
            font-weight: 700;
            color: white;
            text-align: center;
            transition: all 0.3s ease;
        }
        .red { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .blue { background: linear-gradient(135deg, #007bff, #00bfff); }
        .box:hover {
            transform: scale(1.03);
            box-shadow: 0 0 25px rgba(0,0,0,0.2);
        }
        .label {
            pointer-events: none; /* biar klik kena tombol di atas */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Buat label sebagai variable agar tidak memecah string literal
    red_label = "🍝 Eat uncooked pasta\n(Image Classification)"
    blue_label = "🥤 Drink salted coke\n(Object Detection)"

    col1, col2 = st.columns(2, gap="large")
    with col1:
        # Tombol di atas kotak — tombol menangkap klik user
        if st.button(red_label, key="btn_classify"):
            st.session_state.page = "classify"
            st.experimental_rerun()
        # Kotak visual (CSS) di bawah tombol
        st.markdown('<div class="box red"><div class="label"></div></div>', unsafe_allow_html=True)

    with col2:
        if st.button(blue_label, key="btn_detect"):
            st.session_state.page = "detect"
            st.experimental_rerun()
        st.markdown('<div class="box blue"><div class="label"></div></div>', unsafe_allow_html=True)

# ====== CLASSIFY PAGE ======
elif st.session_state.page == "classify":
    st.title("🍝 Image Classification Mode")
    if st.button("⬅️ Kembali ke Menu Awal"):
        st.session_state.page = "home"
        st.experimental_rerun()

    # Tampilkan info import YOLO error jika ada (tidak kritikal untuk klasifikasi)
    if not YOLO_AVAILABLE:
        st.info("YOLO tidak terpasang di environment — hanya klasifikasi yang tersedia.")
    uploaded_file = st.file_uploader("Unggah gambar untuk diklasifikasi", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="📸 Gambar yang diupload", use_column_width=True)
            model = load_classifier_model()
            with st.spinner("🧩 Sedang melakukan klasifikasi..."):
                img_resized = img.resize((128, 128))
                img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
                img_array = np.expand_dims(img_array, axis=0) / 255.0
                prediction = model.predict(img_array)
                class_index = int(np.argmax(prediction))
                prob = float(np.max(prediction))
            st.success("✅ Klasifikasi Berhasil!")
            st.write("### Hasil Prediksi:", class_index)
            st.write("### Probabilitas:", f"{prob:.4f}")
        except Exception as e:
            st.error(f"Gagal melakukan klasifikasi: {e}")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")

# ====== DETECT PAGE ======
elif st.session_state.page == "detect":
    st.title("🥤 Object Detection Mode (YOLO)")
    if st.button("⬅️ Kembali ke Menu Awal"):
        st.session_state.page = "home"
        st.experimental_rerun()

    if not YOLO_AVAILABLE:
        st.error("Model YOLO tidak tersedia di server ini.")
    uploaded_file = st.file_uploader("Unggah gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="📸 Gambar yang diupload", use_column_width=True)
            yolo = load_yolo_model()
            if yolo:
                with st.spinner("🔍 Sedang mendeteksi objek..."):
                    results = yolo.predict(img, verbose=False)
                    result_img = results[0].plot()
                st.image(result_img, caption="Hasil Deteksi", use_column_width=True)
            else:
                st.error("⚠️ YOLO tidak dapat dijalankan di environment ini.")
        except Exception as e:
            st.error(f"Gagal melakukan deteksi: {e}")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")
