# Gunakan image python
FROM python:3.9-slim

# Install dependencies
RUN pip install flask tensorflow streamlit requests Pillow

# Salin aplikasi Flask dan Streamlit
COPY app.py /app/app.py
COPY app_streamlit.py /app/app_streamlit.py

# Set working directory
WORKDIR /app

# Expose port untuk Flask dan Streamlit
EXPOSE 5000 8501

# Perintah untuk menjalankan Flask API dan Streamlit secara bersamaan
CMD ["bash", "-c", "flask run --host=0.0.0.0 & streamlit run app_streamlit.py"]
