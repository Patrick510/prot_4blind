let audioRecorder;
let audioChunks = [];
let audioBlob;

// Função para abrir a câmera
function abrirCamera() {
  const video = document.getElementById("video");
  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "environment" } })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((error) => console.error("Erro ao acessar a câmera: ", error));
}

// Função para capturar a imagem
function capturarImagem() {
  const canvas = document.getElementById("canvas");
  const video = document.getElementById("video");
  const contexto = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  contexto.drawImage(video, 0, 0, canvas.width, canvas.height);
}

// Função para enviar a imagem e o áudio
function enviarImagem() {
  const canvas = document.getElementById("canvas");
  const formData = new FormData();

  // Envia a imagem
  canvas.toBlob((imageBlob) => {
    formData.append("file", imageBlob, "captura.png");

    // Envia o áudio, se disponível
    if (audioBlob) {
      formData.append("audio", audioBlob, "gravacao.mp3"); // Enviando como MP3
    }

    // Envia ambos (imagem e áudio) para o servidor
    fetch("/upload", {
      // Corrija o endpoint conforme necessário
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => console.log("Imagem e Áudio enviados: ", data))
      .catch((error) =>
        console.error("Erro ao enviar a imagem e áudio: ", error)
      );
  }, "image/png");
}

// Função para iniciar a gravação de áudio
function iniciarGravacao() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      audioRecorder = new MediaRecorder(stream);
      audioRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };
      audioRecorder.onstop = () => {
        audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        converterParaMP3(audioBlob); // Converte para MP3 após a gravação
      };
      audioRecorder.start();
    })
    .catch((error) => console.error("Erro ao acessar o microfone: ", error));
}

// Função para parar a gravação de áudio
function pararGravacao() {
  if (audioRecorder) {
    audioRecorder.stop();
  }
}

function converterParaMP3(wavBlob) {
  // Cria um objeto de leitura de arquivo
  const reader = new FileReader();
  reader.onload = function (e) {
    const wavData = e.target.result; // Resultado é um ArrayBuffer

    // Converte para MP3 usando a biblioteca LameJS
    const mp3Encoder = new lamejs.Mp3Encoder(1, 44100, 128); // 1 canal, 44.1kHz, 128kbps
    const mp3Data = [];
    const wav = new Uint8Array(wavData); // Converte o ArrayBuffer para Uint8Array
    const buffer = lamejs.WavHeader.readHeader(wav); // Lê o cabeçalho WAV
    const samples = new Int16Array(
      wav.buffer,
      buffer.dataOffset,
      buffer.dataLength / 2
    ); // Converte os dados WAV para o formato de amostras PCM

    let mp3Buffer = mp3Encoder.encodeBuffer(samples); // Codifica as amostras para MP3
    mp3Data.push(new Int8Array(mp3Buffer)); // Adiciona o buffer de MP3 aos dados

    mp3Buffer = mp3Encoder.flush(); // Finaliza a codificação do MP3
    mp3Data.push(new Int8Array(mp3Buffer)); // Adiciona o buffer final de MP3

    const mp3Blob = new Blob(mp3Data, { type: "audio/mp3" }); // Cria o Blob MP3
    mostrarAudioGravado(mp3Blob); // Exibe o áudio MP3 gravado
    audioBlob = mp3Blob; // Atualiza a variável audioBlob com o áudio MP3
  };

  reader.readAsArrayBuffer(wavBlob); // Carrega o arquivo como ArrayBuffer
}

// Função para mostrar o reprodutor de áudio gravado
function mostrarAudioGravado(audioBlob) {
  const audioContainer = document.getElementById("audioContainer");

  // Criando um elemento de áudio
  const audioElement = document.createElement("audio");
  audioElement.controls = true; // Exibe controles (play, pause, volume)
  const audioUrl = URL.createObjectURL(audioBlob);
  audioElement.src = audioUrl;

  // Limpa o container e adiciona o novo reprodutor
  audioContainer.innerHTML = ""; // Limpa qualquer áudio anterior
  audioContainer.appendChild(audioElement);
}
