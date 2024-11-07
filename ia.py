import google.generativeai as genai
import os
import requests
import re
from dotenv import load_dotenv as ld

ld()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

images_url = [
    "1. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/f8f81621-4de7-4dd2-8731-e8cf52cd6dc3.jpg",
    "2. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/afb6bfca-b3cf-4973-9ef9-b12a404ea5a3.jpg",
    "3. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/c0736897-e34f-4283-af29-76314446cd57.jpg",
    "4. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/0929d3bf-38c9-4f3e-acc7-1787da793c38.jpg",
    "5. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/0dc3bede-2644-4d32-bfc8-c78bafa96150.jpg",
    "6. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/26b4264c-4671-45ae-9e2e-f142af5338c0.jpg",
    "7. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/980f0c4d-68a5-4362-84c1-4da0c3f2dd84.jpg",
    "8. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/985bc9a9-c354-4364-ba42-ca3d705248da.jpg",
    "9. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/f63fc2b9-926f-4721-a7c1-b1b04039a742.jpg",
    "10. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/d71b31e8-9b84-434a-8bfe-65cc4da81efb.jpg",
    "11. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/e317d379-84c6-4428-b811-5489f09cfaab.jpg",
    "12. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/cc902db2-b0a1-43c0-abae-e3476468a4e6.jpg",
    "13. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/fa1b7afa-9eee-48ed-ab4a-ae3cfd311194.jpg",
    "14. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/1b500d41-5835-48ab-9786-af417f2426fe.jpg",
    "15. https://resized-images.autoconf.com.br/1440x0/filters:format(webp)/veiculos/fotos/520661/fad1b636-661b-4bd5-bf3b-b6360d607e81.jpg",
]

def limpa_urls(urls):
    return [re.sub(r"^\d+\.\s*", "", url).strip("[]") for url in urls]

images_url = limpa_urls(images_url)

print(images_url)

images = []

def baixa_imagem(url, numero):
    response = requests.get(url)
    path = f'image{numero}.jpg'
    with open(path, "wb") as file:
        file.write(response.content)
    return path

def processa_imagens(urls):
    paths = []
    try:
        for i, url in enumerate(urls, start=1):
            image_path = baixa_imagem(url, i)  
            paths.append((image_path, url))  

        responses = []
        for path, url in paths:
            genai_image = genai.upload_file(path=path, display_name="carro")
            response = model.generate_content([
                genai_image, 
                url,
                "Pode analisar essa imagem e me dizer se ela é a traseira de um carro visto de lado ou completamente de costas? "
                "Se o carro estiver completamente de costas responda com 'sim2' mais o URL da imagem, se for de lado 'sim' mais o URL, "
                "senão 'não' mais o URL da imagem em português BR."
            ])
            responses.append((response.text, url))
            print(f"> {response.text}")

    finally:
        for path, _ in paths:
            os.remove(path)

    return responses

responses = processa_imagens(images_url)

for image in images:
    os.remove(image.path)