import os
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ===== KONFIGURASI DASAR =====
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

# ===== STATE HALAMAN =====
if "page" not in st.session_state:
    st.session_state.page = "home"

def goto(page):
    st.session_state.page = page
    st.experimental_rerun()

# Hilangkan margin/padding bawaan
st.markdown("""
    <style>
    .block-container {padding:0; margin:0;}
    header, footer {visibility:hidden;}
    .full-container {height:100vh; width:100vw;}
    </style>
    """, unsafe_allow_html=True)

# ====== HOME PAGE ======
if st.session_state.page == "home":
    st.markdown("""
        <style>
        .full-container {
            display:grid;
            grid-template-columns:1fr 1fr;
            height:100vh;
            width:100vw;
            margin:0;
            overflow:hidden;
        }
        .side {
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:2.2rem;
            font-weight:700;
            color:white;
            text-align:center;
            cursor:pointer;
            transition:all 0.25s ease;
            user-select: none;
        }
        .side:hover {transform:scale(1.03); filter:brightness(1.03);}
        .red {background:linear-gradient(135deg,#ff2b2b,#ff6b6b);}
        .blue {background:linear-gradient(135deg,#007bff,#00bfff);}
        </style>

        <div class="full-container">
            <div class="side red" id="redSide">
                🍝 Eat uncooked pasta<br>(Image Classification)
            </div>
            <div class="side blue" id="blueSide">
                🥤 Drink salted coke<br>(Object Detection)
            </div>
        </div>

        <script>
        // Kirim pesan postMessage ke parent
        document.getElementById("redSide").onclick = () => {
            window.parent.postMessage({streamlitMessage: "goto_classify"}, "*");
        };
        document.getElementById("blueSide").onclick = () => {
            window.parent.postMessage({streamlitMessage: "goto_detect"}, "*");
        };

        // Saat menerima message dari parent streamlit (opsional)
        window.addEventListener("message", (event) => {
            // no-op, placeholder if needed
        });
        </script>
    """, unsafe_allow_html=True)

    # === GANTI: gunakan st.query_params (bukan experimental) ===
    msg = st.query_params.get("msg", [None])[0]
    if msg == "goto_classify":
        goto("classify")
    elif msg == "goto_detect":
        goto("detect")

    # Listener JS untuk menulis query param dan memicu Streamlit menangkapnya
    st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            const data = event.data.streamlitMessage;
            if (data === "goto_classify" || data === "goto_detect") {
                const newUrl = new URL(window.location);
                newUrl.searchParams.set("msg", data);
                // ubah location sehingga Streamlit membaca st.query_params tanpa kehilangan session_state
                window.location.href = newUrl;
            }
        });
        </script>
    """, unsafe_allow_html=True)

# ====== IMAGE CLASSIFICATION PAGE ======
elif st.session_state.page == "classify":
    st.title("🍝 Image Classification")
    if st.button("⬅️ Kembali"):
        goto("home")

    uploaded_file = st.file_uploader("Unggah gambar", type=["jpg","jpeg","png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar diunggah", use_column_width=True)
        model = load_classifier_model()
        img_resized = img.resize((128,128))
        arr = tf.keras.preprocessing.image.img_to_array(img_resized)
        arr = np.expand_dims(arr,0)/255.0
        with st.spinner("Klasifikasi..."):
            pred = model.predict(arr)
            idx = int(np.argmax(pred))
            prob = float(np.max(pred))
        st.success("✅ Hasil Klasifikasi")
        st.write("Kelas:", idx)
        st.write("Probabilitas:", f"{prob:.4f}")

# ====== OBJECT DETECTION PAGE ======
elif st.session_state.page == "detect":
    st.title("🥤 Object Detection")
    if st.button("⬅️ Kembali"):
        goto("home")

    if not YOLO_AVAILABLE:
        st.error(f"YOLO tidak tersedia: {YOLO_IMPORT_ERROR}")
    uploaded_file = st.file_uploader("Unggah gambar", type=["jpg","jpeg","png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Gambar diunggah", use_column_width=True)
        yolo = load_yolo_model()
        if yolo:
            with st.spinner("Mendeteksi..."):
                results = yolo.predict(img, verbose=False)
                result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_column_width=True)
        else:
            st.error("Model YOLO tidak dapat dijalankan di environment ini.")
