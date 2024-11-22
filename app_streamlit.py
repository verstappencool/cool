import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# URL API Flask
api_url = "http://localhost:5000/predict"

st.title("Prediksi Kucing Besar")

# Upload gambar
uploaded_file = st.file_uploader("Pilih gambar kucing besar", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Menampilkan gambar yang diupload
    img = Image.open(uploaded_file)
    st.image(img, caption="Gambar yang Diupload", use_column_width=True)

    # Kirim gambar ke API Flask
    files = {'file': uploaded_file.getvalue()}
    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        result = response.json()
        st.subheader("Hasil Prediksi:")
        st.write(f"**Prediksi Kelas**: {result['predicted_class']}")
        st.write(f"**Probabilitas**: {result['probability'] * 100:.2f}%")

        # Tampilkan probabilitas untuk semua kelas
        st.write("**Probabilitas untuk Setiap Kelas**:")
        for class_name, prob in result['class_probabilities'].items():
            st.write(f"{class_name}: {prob * 100:.2f}%")
    else:
        st.error("Terjadi kesalahan dalam memprediksi gambar.")
