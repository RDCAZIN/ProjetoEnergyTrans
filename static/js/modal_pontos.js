const botoesDetalhes =
document.querySelectorAll(".btn-detalhes")

const modalOverlay =
document.getElementById("modal-overlay")

const fecharModal =
document.getElementById("fechar-modal")

const modalNome =
document.getElementById("modal-nome")

const modalEndereco =
document.getElementById("modal-endereco")

const modalMateriais =
document.getElementById("modal-materiais")

const modalHorario =
document.getElementById("modal-horario")

const modalPontoId =
document.getElementById("modal-ponto-id")

// ABRIR MODAL

botoesDetalhes.forEach(botao => {

    botao.addEventListener("click", () => {
        modalPontoId.value =
        botao.dataset.id

        modalNome.textContent =
        botao.dataset.nome

        modalEndereco.textContent =
        botao.dataset.endereco

        modalMateriais.textContent =
        botao.dataset.materiais

        modalHorario.textContent =
        botao.dataset.horario

        modalOverlay.style.display = "flex"

    })

})

// FECHAR MODAL

fecharModal.addEventListener("click", () => {

    modalOverlay.style.display = "none"

})

// FECHAR AO CLICAR FORA

modalOverlay.addEventListener("click", (event) => {

    if (event.target === modalOverlay) {

        modalOverlay.style.display = "none"

    }

})