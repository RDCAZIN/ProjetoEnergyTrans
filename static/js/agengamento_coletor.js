// BOTÕES DOS PONTOS
const botoesPonto =
document.querySelectorAll(".btn-ponto")

// BOTÕES DE CONFIRMAR ENTREGA
const botoesConfirmar =
document.querySelectorAll(".btn-confirmar")

// MODAL
const modal =
document.getElementById("modal-overlay")

// INPUT HIDDEN
const inputAgendamento =
document.getElementById("agendamento-id")

// =========================
// ABRIR/CLOSE AGENDAMENTOS
// =========================

botoesPonto.forEach(botao => {

    botao.addEventListener("click", () => {

        const agendamentos =
        botao.nextElementSibling

        if (
            agendamentos.style.display === "block"
        ) {

            agendamentos.style.display = "none"

        } else {

            agendamentos.style.display = "block"

        }

    })

})

// =========================
// ABRIR MODAL
// =========================

botoesConfirmar.forEach(botao => {

    botao.addEventListener("click", () => {

        // PEGA ID DO AGENDAMENTO
        const agendamentoId =
        botao.dataset.id

        // COLOCA NO INPUT HIDDEN
        inputAgendamento.value =
        agendamentoId

        // ABRE MODAL
        modal.style.display = "flex"

    })

})

// =========================
// FECHAR MODAL CLICANDO FORA
// =========================

modal.addEventListener("click", (event) => {

    if (event.target === modal) {

        modal.style.display = "none"

    }

})