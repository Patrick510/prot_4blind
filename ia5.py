import requests

# Função para pegar a frase simples da Gemini API
def get_simple_phrase():
    url = "https://api.gemini.com/v1/pubticker/btcusd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return f"O preço atual do BTC/USD é: {data['last']}"
    else:
        return "Desculpe, houve um erro ao obter o preço."

# Chama a função e exibe a frase simples
print(get_simple_phrase())
