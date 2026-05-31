window.addEventListener("load", () => {

    // =========================
    // IFRAME DO FOLIUM
    // =========================
    
    console.log("JS NOVO CARREGADO")
    const iframe =
    document.querySelector(".mapa iframe")

    // WINDOW INTERNO DO MAPA

    const mapaWindow =
    iframe.contentWindow

    // DOCUMENTO INTERNO

    const mapaDocument =
    mapaWindow.document

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

    btnAgendar.addEventListener(
        "click",
        () => {

            console.log(
                "clicou no botão"
            )

            // VERIFICAR PONTO

            if (!pontoSelecionado) {

                alert(
                    "Selecione um ponto no mapa"
                )

                return

            }

            // INSERIR ID

            pontoIdInput.value =
            pontoSelecionado.id

            // MOSTRAR MODAL

            modal.style.display =
            "flex"

        }
    )

    // =========================
    // FECHAR MODAL
    // =========================

    const btnFechar =
    document.getElementById(
        "fechar-modal"
    )

    btnFechar.addEventListener(
        "click",
        () => {

            modal.style.display =
            "none"

        }
    )

    // =========================
    // FECHAR FORA
    // =========================

    modal.addEventListener(
        "click",
        (event) => {

            if (
                event.target === modal
            ) {

                modal.style.display =
                "none"

            }

        }
    )

    // =========================
    // LOCALIZAÇÃO USUÁRIO
    // =========================

    const btnLocalizacao =
    document.getElementById(
        "btn-localizacao"
    )

    const textoLocalizacao =
    document.getElementById(
        "texto-localizacao"
    )

    // CLICK

    btnLocalizacao.addEventListener(
        "click",
        () => {

            // GEOLOCATION

            if (
                navigator.geolocation
            ) {

                navigator.geolocation.getCurrentPosition(

                    (posicao) => {

                        const latitude =
                        posicao.coords.latitude

                        const longitude =
                        posicao.coords.longitude

                        console.log(
                            latitude,
                            longitude
                        )

                        // MAPA LEAFLET

                        const mapaLeaflet =
                        Object.values(
                            mapaWindow
                        ).find(
                            item =>
                            item instanceof mapaWindow.L.Map
                        )

                        // CENTRALIZAR

                        mapaLeaflet.setView(
                            [latitude, longitude],
                            15
                        )

                        // MARCADOR

                        mapaWindow.L.marker(
                            [latitude, longitude]
                        )
                        .addTo(mapaLeaflet)
                        .bindPopup(
                            "Sua localização"
                        )
                        .openPopup()

                        // TEXTO
                        fetch(`/buscar_endereco?latitude=${latitude}&longitude=${longitude}`)
                            .then(resposta => resposta.json())
                            .then(dados => {
                                console.log(dados)
                                textoLocalizacao.innerText = `${dados.bairro} - ${dados.cidade}`
                            })
                    },

                    () => {

                        alert(
                            "Não foi possível acessar sua localização"
                        )

                    }

                )

            } else {

                alert(
                    "Geolocalização não suportada"
                )

            }

        }
    )

})