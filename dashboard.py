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
        # jangan panggil st.* di dalam fungsi cache_resource kalau bukan di UI; 
        # tetap mengembalikan None, None dan beri info di UI nanti
        return None, None, str(e)

# catatan: agar kita bisa menampilkan error message, panggil load_models() di luar try UI
models = load_models()
# jika load_models mengembalikan 3 nilai (error pesan), sesuaikan:
if isinstance(models, tuple) and len(models) == 3:
    yolo_model, classifier, load_err = models
else:
    # kompatibilitas bila load_models mengembalikan 2 nilai
    try:
        yolo_model, classifier = models
        load_err = None
    except Exception:
        yolo_model, classifier, load_err = None, None, "Unknown error saat memuat model."

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Image Classifier & Detection", layout="wide")

# --- Inisialisasi session_state untuk navigasi ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Fungsi navigasi ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Sidebar Navigasi (pakai on_click untuk respons 1-klik) ---
with st.sidebar:
    st.title("🔍 Menu Navigasi")
    st.button("🏠 Home", key="nav_home", on_click=go_to, args=("home",))
    st.button("🖼 Klasifikasi Gambar", key="nav_classify", on_click=go_to, args=("classify",))
    st.button("🎯 Deteksi Objek", key="nav_detect", on_click=go_to, args=("detect",))

# --- Halaman HOME ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Selamat Datang!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Pilih salah satu menu di bawah untuk memulai.</p>", unsafe_allow_html=True)

    # tiga kolom: tombol ditaruh di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)  # jarak atas
        # gunakan on_click agar langsung bekerja sekali klik
        st.button("🖼 Buka Klasifikasi Gambar", key="home_open_classify", on_click=go_to, args=("classify",), use_container_width=True)
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        st.button("🎯 Buka Deteksi Objek", key="home_open_detect", on_click=go_to, args=("detect",), use_container_width=True)

# --- Halaman KLASIFIKASI GAMBAR ---
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
            # gunakan use_container_width (ganti deprecated use_column_width)
            st.image(img, caption="Gambar yang diupload", use_container_width=True)

            # Preprocessing dan prediksi
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

# --- Halaman DETEKSI OBJEK ---
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

            # Deteksi objek
            with st.spinner('Memproses Deteksi Objek...'):
                results = yolo_model(img)
                result_img = results[0].plot()

                # Ambil daftar label deteksi
                detected_labels = []
                # results[0].boxes bisa kosong; cek eksistensi
                if hasattr(results[0], "boxes") and results[0].boxes is not None:
                    for box in results[0].boxes:
                        # beberapa versi ultralytics menyimpan .cls sebagai tensor
                        try:
                            class_id = int(box.cls[0])
                        except Exception:
                            # fallback: jika cls langsung skalar
                            class_id = int(box.cls)
                        # names map tersedia di results[0].names
                        label = results[0].names.get(class_id, str(class_id)) if hasattr(results[0], "names") else str(class_id)
                        detected_labels.append(label)

                # tampilkan gambar hasil
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)
                st.success("✅ Deteksi Selesai!")

                # -> Teks tambahan di bawah gambar
                if detected_labels:
                    unique_labels = list(dict.fromkeys(detected_labels))  # pertahankan urutan muncul
                    label_text = ", ".join(unique_labels)
                    total = len(detected_labels)
                    st.markdown(f"### 🧩 Terdeteksi bidak catur: **{label_text}**")
                    st.write(f"Jumlah total objek terdeteksi: **{total}**")
                else:
                    st.warning("Tidak ada objek yang terdeteksi.")

    st.button("⬅ Kembali ke Home", key="back_from_detect", on_click=go_to, args=("home",))
