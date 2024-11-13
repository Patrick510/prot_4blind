import cv2
import numpy as np
from keras._tf_keras.keras.models import load_model

# Desabilitar a notação científica para melhor clareza
np.set_printoptions(suppress=True)

# Carregar o modelo
model = load_model("models/keras_Model.h5", compile=False)

# Carregar os rótulos
class_names = open("models/labels.txt", "r").readlines()

# Carregar a imagem com o OpenCV
image = cv2.imread("imgs/img3.jpg")

# Redimensionar a imagem para 224x224
image = cv2.resize(image, (224, 224))

# Converter a imagem de BGR (padrão OpenCV) para RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Normalizar a imagem
normalized_image_array = (image.astype(np.float32) / 127.5) - 1

# Preparar a entrada para o modelo
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
data[0] = normalized_image_array

# Fazer a predição
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Exibir o resultado
print("Class:", class_name.strip())
print("Confidence Score:", confidence_score)
