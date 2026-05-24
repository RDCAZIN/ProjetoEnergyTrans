window.addEventListener("load", () => {

    // =========================
    // IFRAME DO FOLIUM
    // =========================

    const iframe =
    document.querySelector(".mapa iframe")

    // DOCUMENTO INTERNO DO MAPA

    const mapaDocument =
    iframe.contentWindow.document

    // =========================
    // MARCADORES
    // =========================

    const marcadores =
    mapaDocument.querySelectorAll(
        ".leaflet-marker-icon"
    )

    console.log(marcadores)

    // =========================
    // CARD
    // =========================

    const nomePonto =
    document.getElementById("nome-ponto")

    const enderecoPonto =
    document.getElementById("endereco-ponto")

    const materiaisPonto =
    document.getElementById("materiais-ponto")

    const horarioPonto =
    document.getElementById("horario-ponto")

    // =========================
    // BOTÃO AGENDAR
    // =========================

    const btnAgendar =
    document.getElementById("btn-agendar")

    // =========================
    // MODAL
    // =========================

    const modal =
    document.getElementById(
        "modal-agendamento"
    )

    // =========================
    // INPUT HIDDEN
    // =========================

    const pontoIdInput =
    document.getElementById(
        "ponto-id"
    )

    // =========================
    // PONTO SELECIONADO
    // =========================

    let pontoSelecionado = null

    // =========================
    // CLIQUE NOS MARCADORES
    // =========================

    marcadores.forEach((marcador, index) => {

        marcador.addEventListener("click", () => {

            // PEGAR PONTO

            const ponto =
            pontos[index]

            // SALVAR PONTO

            pontoSelecionado =
            ponto

            // ATUALIZAR CARD

            nomePonto.innerText =
            ponto.nome

            enderecoPonto.innerText =
            ponto.endereco

            materiaisPonto.innerText =
            "Materiais: " +
            ponto.materiais

            horarioPonto.innerText =
            "Horário: " +
            ponto.horario

        })

    })

    // =========================
    // ABRIR MODAL
    // =========================

    btnAgendar.addEventListener("click", () => {
        console.log("clicou no botão")
        // VERIFICAR PONTO

        if (!pontoSelecionado) {

            alert(
                "Selecione um ponto no mapa"
            )

            return

        }

        // INSERIR ID DO PONTO

        pontoIdInput.value =
        pontoSelecionado.id

        // MOSTRAR MODAL

        modal.style.display =
        "flex"

    })

    

})

// FECHAR MODAL

const btnFechar =
document.getElementById("fechar-modal")

const modal =
document.getElementById("modal-agendamento")

btnFechar.addEventListener("click", () => {

    modal.style.display = "none"

})

// FECHAR AO CLICAR FORA

modal.addEventListener("click", (event) => {

    if (
        event.target === modal
    ) {

        modal.style.display = "none"

    }

})