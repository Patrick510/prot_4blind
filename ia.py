import google.generativeai as genai # pip install -q -U google-generativeai
import os
import requests
from dotenv import load_dotenv as ld
import pyttsx3
import cv2

ld()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def processa_imagem(image):
    try:
        
        genai_image = genai.upload_file(path=image, display_name="imagem")
        response = model.generate_content([
            genai_image, 
            "Me descreva o ambiente que eu estou agora, com base na imagem. Sou uma pessoa cego, de forma simples e objetiva."
        ])
        
        print(f"> {response.text}")

        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  

        engine.say(response.text)
        engine.save_to_file(response.text, 'descricao.mp3')  
        engine.runAndWait()

        print("Descrição salva como 'descricao.mp3'")

    finally:
        print("resposta ja dada fi")
        #os.remove(image_path)

camera = cv2.VideoCapture(0)

#cv2.namedWindow("preview")

ret, frame = camera.read()

if not ret:
  print("Erro ao capturar a imagem")

cv2.imwrite("imagem.jpg", frame)

camera.release()

print("imagem capturada")

processa_imagem("imagem.jpg")
