from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf

# Inisialisasi Flask
app = Flask(__name__)

# Memuat model yang telah dilatih
model = load_model('my_model-2.h5')

# Kelas yang diprediksi
class_names = ['Cheetah', 'Jaguar', 'Jaguar_Hitam', 'Leopard', 'Lion', 'Puma', 'Tiger']

# Fungsi prediksi yang dioptimalkan
@tf.function
def predict_image(img_array):
    return model(img_array)

# Endpoint untuk memprediksi gambar
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Memuat gambar
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Melakukan prediksi
    predictions = predict_image(img_array)
    predictions_np = predictions.numpy()[0]
    predicted_class_index = np.argmax(predictions_np)
    predicted_class = class_names[predicted_class_index]
    predicted_prob = np.max(predictions_np)

    return jsonify({
        'predicted_class': predicted_class,
        'probability': predicted_prob,
        'class_probabilities': {class_names[i]: float(predictions_np[i]) for i in range(len(class_names))}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Flask API berjalan di port 5000
