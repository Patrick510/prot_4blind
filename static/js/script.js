const fileInput = document.getElementById("file");
const uploadedImg = document.querySelector(".uploadedImg");
const submit = document.querySelector(".submit");
const loadingMessage = document.querySelector(".loading-message"); // Exibir mensagem de carregamento
const descriptionContainer = document.querySelector(".description-container"); // Exibir descrição gerada

// Exibindo a imagem após a seleção
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    uploadedImg.src = e.target.result;
  };

  reader.readAsDataURL(file);
});

// Enviando a imagem para o servidor ao clicar no botão
submit.addEventListener("click", async (e) => {
  e.preventDefault(); // Impede o comportamento padrão de submit do formulário

  const formData = new FormData();
  const file = fileInput.files[0];

  if (!file) {
    alert("Por favor, selecione uma imagem.");
    return;
  }

  formData.append("image", file);

  // Exibir mensagem de carregamento
  loadingMessage.style.display = "block";

  try {
    const response = await fetch("http://10.8.34.203:5000/send", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.message === "success") {
      console.log("Imagem enviada com sucesso!");
      uploadedImg.src = data.image_url; // Atualiza a imagem no front-end
      // Exibe a descrição gerada
      descriptionContainer.innerHTML = `<p>${data.description}</p>`;
    } else {
      console.error("Erro ao processar a imagem:", data.message);
      alert("Erro ao processar a imagem.");
    }
  } catch (error) {
    console.error("Erro ao enviar imagem:", error);
    alert("Erro de conexão com o servidor.");
  } finally {
    // Esconde a mensagem de carregamento
    loadingMessage.style.display = "none";
    fileInput.value = ""; // Limpa o campo de input após o envio
  }
});
