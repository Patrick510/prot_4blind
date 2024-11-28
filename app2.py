import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pyttsx3
from dotenv import load_dotenv as ld
import speech_recognition as sr

xapp = Flask(__name__)
CORS(xapp)

ld()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
xapp.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@xapp.route("/")
def home():
    print("Rota principal / acessada")
    return render_template("index2.html")


def transcrever_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="pt-BR")
            arq = open("transcricao.txt", "w")
            arq.write(text)
            arq.close()
            print(text)
            return text  # Retorna o texto transcrito
        except sr.UnknownValueError:
            print("Google Speech Recognition não conseguiu entender o áudio")
            return None  # Retorna None em caso de erro

# Rota para enviar arquivos (imagem e áudio)
@xapp.route("/upload", methods=["POST"])
def upload_files():
    if 'image' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Nenhum arquivo de imagem ou áudio encontrado"})
    
    image_file = request.files['image']
    audio_file = request.files['audio']
    
    if image_file.filename == '' or audio_file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"})
    
    # Definir os caminhos para salvar os arquivos
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    
    # Salvar os arquivos
    image_file.save(image_path)
    audio_file.save(audio_path)
    
    print(f"Imagem salva em: {image_path}")
    print(f"Áudio salvo em: {audio_path}")
    
    # Processar a imagem e o áudio
    texto_audio = transcrever_audio(audio_path)  # Transcrever áudio
    
    if texto_audio is None:
        return jsonify({"error": "Falha na transcrição do áudio"})
    
    try:
      # Processar a imagem com IA
      genai_image = genai.upload_file(path=image_path, display_name="imagem")
      
      # Gerar uma resposta com base na imagem e no áudio transcrito
      response = model.generate_content([genai_image, texto_audio])
      
      print(f"IA respondeu: {response.text}")

      # Gerar áudio da resposta (descrição)
      engine = pyttsx3.init()
      voices = engine.getProperty('voices')
      engine.setProperty('voice', voices[0].id)  
      engine.say(response.text)
      engine.save_to_file(response.text, 'descricao.mp3')  
      engine.runAndWait()

      print("Descrição salva como 'descricao.mp3'")

      # Enviar resposta com os arquivos
      return jsonify({
          "message": "Imagem e áudio carregados com sucesso", 
          "image_filename": image_file.filename, 
          "audio_filename": audio_file.filename,
          "descricao_audio": "descricao.mp3",
          "descricao_texto": response.text  # Incluir o texto gerado como descrição
      })

    except Exception as e:
        print(f"Erro ao processar imagem ou áudio: {e}")
        return jsonify({"error": "Erro ao processar a imagem ou áudio"})

if __name__ == "__main__":
    xapp.run(debug=True, host="0.0.0.0")
