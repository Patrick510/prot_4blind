import speech_recognition as sr

def transcrever_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError:
        return "Erro na solicitação ao serviço de reconhecimento"

# Teste a função
audio_path = 'C:/estudos/4 PERIODO/extensao/prot_4blind/uploads/gravacao.wav'
texto_audio = transcrever_audio(audio_path)
print(texto_audio)
