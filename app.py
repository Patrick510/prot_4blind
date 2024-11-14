import google.generativeai as genai
import os
from dotenv import load_dotenv as ld
import pyttsx3
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

xapp = Flask(__name__)
CORS(xapp)

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

@xapp.route("/")
def home():
    return render_template("index.html")

@xapp.route("/send", methods=["POST"])
def send():
    try:
        image = request.files["image"]
        if not image:
            return jsonify({"message": "Nenhuma imagem foi enviada."}), 400
        
        image_path = f"image.{image.filename.split('.')[-1]}"
        image.save(image_path)

        processa_imagem(image_path)

        # Retorne a URL da imagem para ser exibida no front-end
        return jsonify({"message": "success", "image_url": f"/uploads/{image_path}", "description_url": "/descricao.mp3"})
    
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return jsonify({"message": "Erro ao processar a imagem."}), 500

# Adicionando uma rota para servir as imagens
@xapp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(os.getcwd(), filename)

# Rota para servir o arquivo de descrição (MP3)
@xapp.route("/descricao.mp3")
def descricao_file():
    return send_from_directory(os.getcwd(), 'descricao.mp3')

if __name__ == "__main__":
    xapp.run(debug=True, host="0.0.0.0")
