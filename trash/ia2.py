import google.generativeai as genai # pip install -q -U google-generativeai
import os
import requests
from dotenv import load_dotenv as ld
import pyttsx3

ld()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def baixa_imagem(url):
    response = requests.get(url)
    path = 'imagem.jpg'  # Nome fixo para a imagem baixada
    with open(path, "wb") as file:
        file.write(response.content)
    return path

def processa_imagem(url):
    try:
        image_path = baixa_imagem(url)
        
        genai_image = genai.upload_file(path=image_path, display_name="imagem")
        response = model.generate_content([
            genai_image, 
            url,
            "Me descreva o ambiente que eu estou agora, com base na imagem. Sou uma pessoa cego, de forma simples e objetiva."
        ])
        
        print(f"> {response.text}")

        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  

        # Gera o áudio
        engine.say(response.text)
        engine.save_to_file(response.text, 'descricao.mp3')  # Salva como arquivo MP3
        engine.runAndWait()

        print("Descrição salva como 'descricao.mp3'")

    finally:
        os.remove(image_path)

# Exemplo de uso
url_imagem = "https://imagens.usp.br/wp-content/uploads/0701_odontosalaaula005.jpg"
processa_imagem(url_imagem)
