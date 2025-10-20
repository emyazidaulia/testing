import streamlit as st
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# ==========================
# Konfigurasi Global
# ==========================
CLASS_NAMES = ['Kebakaran Hutan', 'Bukan Kebakaran Hutan']  # sesuaikan

# ==========================
# Load Models (basecode)
# ==========================
@st.cache_resource
def load_models():
    try:
        yolo_model = YOLO("model/Muhammad Yazid Aulia_Laporan 4.pt")  # Model deteksi objek
        classifier = tf.keras.models.load_model("model/Muhammad Yazid Aulia_Laporan 2.h5")  # Model klasifikasi
        return yolo_model, classifier
    except Exception as e:
        # Jangan panggil st.* di dalam fungsi cache_resource kalau bukan di UI
        return None, None, str(e)

# Load model dan tangani error
models = load_models()
if isinstance(models, tuple) and len(models) == 3:
    yolo_model, classifier, load_err = models
else:
    try:
        yolo_model, classifier = models
        load_err = None
    except Exception:
        yolo_model, classifier, load_err = None, None, "Unknown error saat memuat model."

# ==========================
# Konfigurasi Halaman
# ==========================
st.set_page_config(page_title="Image Classifier & Detection", layout="wide")

# ==========================
# Navigasi (Session State)
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# ==========================
# Sidebar Navigasi
# ==========================
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    st.button("🏠 Home", key="nav_home", on_click=go_to, args=("home",))
    st.button("🖼 Klasifikasi Gambar", key="nav_classify", on_click=go_to, args=("classify",))
    st.button("🎯 Deteksi Objek", key="nav_detect", on_click=go_to, args=("detect",))

# ==========================
# Halaman HOME
# ==========================
if st.session_state.page == "home":
    # CSS kustom untuk tampilan modern
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            margin-top: 30px;
            color: #ffffff;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #dcdcdc;
            margin-bottom: 40px;
        }
        .menu-container {
            display: flex;
            justify-content: center;
            gap: 50px;
            flex-wrap: wrap;
        }
        .menu-card {
            background-color: #ff4b4b;
            width: 320px;
            height: 220px;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .menu-card:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(255,255,255,0.2);
        }
        .blue {
            background-color: #3b82f6;
        }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #ccc;
            margin-top: 60px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Konten utama
    st.markdown("<div class='title'>🔥 Selamat Datang di Aplikasi Deteksi Gambar</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Pilih salah satu menu di bawah untuk memulai analisis gambar Anda.</div>", unsafe_allow_html=True)

    # Menu interaktif
    st.markdown("""
        <div class='menu-container'>
            <div class='menu-card' onclick="window.parent.location.href='?nav=classify'">🖼️<br>Klasifikasi Gambar</div>
            <div class='menu-card blue' onclick="window.parent.location.href='?nav=detect'">🎯<br>Deteksi Objek</div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>Dibuat dengan ❤️ menggunakan Streamlit | Versi 2.0</div>", unsafe_allow_html=True)

    # --- Navigasi event handler ---
    # Streamlit tidak otomatis tangkap onclick JS, jadi tambahkan tombol tersembunyi sebagai fallback
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        if st.button("🖼 Buka Klasifikasi (opsi alternatif)", use_container_width=True):
            go_to("classify")
        if st.button("🎯 Buka Deteksi Objek (opsi alternatif)", use_container_width=True):
            go_to("detect")


# ==========================
# Halaman KLASIFIKASI GAMBAR
# ==========================
elif st.session_state.page == "classify":
    st.header("🖼 Menu Klasifikasi Gambar")

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif classifier is None:
        st.warning("Model Klasifikasi tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk klasifikasi", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            with st.spinner('Memproses Klasifikasi...'):
                img_resized = img.resize((128, 128))
                img_array = image.img_to_array(img_resized)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                prediction = classifier.predict(img_array)
                class_index = np.argmax(prediction)
                probability = np.max(prediction)

                if class_index < len(CLASS_NAMES):
                    predicted_class = CLASS_NAMES[class_index]
                    st.success("✅ Klasifikasi Selesai!")
                    st.markdown(f"### Hasil Prediksi: *{predicted_class}*")
                    st.write(f"*Probabilitas:* {probability*100:.2f}%")
                else:
                    st.error("Indeks kelas tidak valid. Pastikan CLASS_NAMES sudah benar.")

    st.button("⬅ Kembali ke Home", key="back_from_classify", on_click=go_to, args=("home",))

# ==========================
# Halaman DETEKSI OBJEK
# ==========================
elif st.session_state.page == "detect":
    st.header("🎯 Menu Deteksi Objek")

    if load_err:
        st.error(f"Gagal memuat model: {load_err}")
    elif yolo_model is None:
        st.warning("Model Deteksi Objek tidak dapat dimuat.")
    else:
        uploaded_file = st.file_uploader("Upload gambar untuk deteksi objek", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            with st.spinner('Memproses Deteksi Objek...'):
                results = yolo_model(img)
                result_img = results[0].plot()

                detected_labels = []
                if hasattr(results[0], "boxes") and results[0].boxes is not None:
                    for box in results[0].boxes:
                        try:
                            class_id = int(box.cls[0])
                        except Exception:
                            class_id = int(box.cls)
                        label = results[0].names.get(class_id, str(class_id)) if hasattr(results[0], "names") else str(class_id)
                        detected_labels.append(label)

                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
                st.success("✅ Deteksi Selesai!")

                if detected_labels:
                    unique_labels = list(dict.fromkeys(detected_labels))
                    label_text = ", ".join(unique_labels)
                    total = len(detected_labels)
                    st.markdown(f"### 🧩 Terdeteksi objek: **{label_text}**")
                    st.write(f"Jumlah total objek terdeteksi: **{total}**")
                else:
                    st.warning("Tidak ada objek yang terdeteksi.")

    st.button("⬅ Kembali ke Home", key="back_from_detect", on_click=go_to, args=("home",))
