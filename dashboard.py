import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Gunakan direktori sementara agar tidak crash
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

# Import YOLO dengan aman
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
    st.warning(f"⚠️ YOLO tidak aktif di environment ini: {e}")
    YOLO_AVAILABLE = False


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


# ==========================
# Konfigurasi halaman
# ==========================
st.set_page_config(page_title="Would You Rather: AI Edition", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"  # home, classify, detect


# ==========================
# Tampilan Awal (Would You Rather)
# ==========================
if st.session_state.page == "home":
    st.markdown(
        """
        <style>
        .choice-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            gap: 2rem;
        }
        .choice {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            font-weight: 700;
            color: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            height: 60vh;
        }
        .choice:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
        }
        .red { background: linear-gradient(135deg, #ff2b2b, #ff6b6b); }
        .blue { background: linear-gradient(135deg, #007bff, #00bfff); }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍝 Eat uncooked pasta\n(Image Classification)", use_container_width=True):
            st.session_state.page = "classify"
            st.rerun()

        st.markdown(
            "<div class='choice red' style='margin-top:-3.5em;'></div>",
            unsafe_allow_html=True
        )

    with col2:
        if st.button("🥤 Drink salted coke\n(Object Detection)", use_container_width=True):
            st.session_state.page = "detect"
            st.rerun()

        st.markdown(
            "<div class='choice blue' style='margin-top:-3.5em;'></div>",
            unsafe_allow_html=True
        )

# ==========================
# Halaman Klasifikasi
# ==========================
elif st.session_state.page == "classify":
    st.title("🍝 Image Classification Mode")
    if st.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.page = "home"
        st.rerun()

    uploaded_file = st.file_uploader("Unggah gambar untuk diklasifikasi", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="📸 Gambar yang diupload", use_container_width=True)

        classifier = load_classifier_model()
        with st.spinner("🧩 Sedang melakukan klasifikasi..."):
            img_resized = img.resize((128, 128))
            img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            prediction = classifier.predict(img_array)
            class_index = np.argmax(prediction)
            probability = np.max(prediction)

        st.success("✅ Klasifikasi Berhasil!")
        st.write("### Hasil Prediksi:", class_index)
        st.write("### Probabilitas:", f"{probability:.4f}")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")

# ==========================
# Halaman Deteksi Objek
# ==========================
elif st.session_state.page == "detect":
    st.title("🥤 Object Detection Mode (YOLO)")
    if st.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.page = "home"
        st.rerun()

    uploaded_file = st.file_uploader("Unggah gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="📸 Gambar yang diupload", use_container_width=True)

        yolo_model = load_yolo_model()
        if yolo_model:
            with st.spinner("🔍 Sedang mendeteksi objek..."):
                results = yolo_model.predict(img, verbose=False)
                result_img = results[0].plot()
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
        else:
            st.error("⚠️ Model YOLO tidak dapat digunakan di server ini.")
    else:
        st.info("📁 Silakan unggah gambar terlebih dahulu.")
