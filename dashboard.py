import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Persiapan environment
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
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

# ============ HALAMAN HOME ============
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
            cursor: pointer;
            position: relative;
        }
        .red { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .blue { background: linear-gradient(135deg, #007bff, #00bfff); }
        .box:hover {
            transform: scale(1.03);
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
        }
        .label {
            z-index: 2;
        }
        .overlay-button {
            position: absolute;
            inset: 0;
            background: transparent;
            border: none;
            cursor: pointer;
            z-index: 3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="container">', unsafe_allow_html=True)

    # ====== KOTAK MERAH (Klasifikasi) ======
    red_click = st.markdown(
        """
        <form action="?page=classify" method="get">
            <button class="overlay-button" type="submit"></button>
            <div class="box red">
                <div class="label">🍝 Eat uncooked pasta<br>(Image Classification)</div>
            </div>
        </form>
        """,
        unsafe_allow_html=True
    )

    # ====== KOTAK BIRU (Deteksi) ======
    blue_click = st.markdown(
        """
        <form action="?page=detect" method="get">
            <button class="overlay-button" type="submit"></button>
            <div class="box blue">
                <div class="label">🥤 Drink salted coke<br>(Object Detection)</div>
            </div>
        </form>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Tangkap query parameter agar klik HTML bisa ubah halaman
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.page = query_params["page"]
        st.experimental_rerun()

# ============ HALAMAN KLASIFIKASI ============
elif st.session_state.page == "classify":
    st.title("🍝 Image Classification Mode")
    if st.button("⬅️ Kembali ke Menu Awal"):
        st.session_state.page = "home"
        st.experimental_rerun()

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

# ============ HALAMAN DETEKSI ============
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
