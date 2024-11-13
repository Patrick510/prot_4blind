import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv as ld
import pyttsx3
import cv2
from datetime import datetime

ld()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        engine.save_to_file(response.text, f'descricao_{timestamp}.mp3')  
        engine.runAndWait()

        print("Descrição salva como 'descricao.mp3'")

    finally:
        print("Resposta já dada.")
        os.remove(image)

camera = cv2.VideoCapture(0)

ret, frame = camera.read()

if not ret:
    print("Erro ao capturar a imagem")
    camera.release()
    exit()

cv2.imwrite("imagem.jpg", frame)

camera.release()

print("Imagem capturada")

processa_imagem("imagem.jpg")
