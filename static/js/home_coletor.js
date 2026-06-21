// =========================
// MODAL EDITAR PONTO
// =========================

const pontoId =
document.getElementById("ponto_id")

const nomePonto =
document.getElementById("nome_ponto")

const enderecoPonto =
document.getElementById("endereco_ponto")

const materiaisPonto =
document.getElementById("materias_ponto")

const horarioPonto =
document.getElementById("horario_ponto")

const botoesPonto =
document.querySelectorAll(".btn-editar")

const modalEditar =
document.getElementById("modal-overlay")

const btnFecharEditar =
document.getElementById("fechar-modal")

// =========================
// ABRIR MODAL EDITAR
// =========================

botoesPonto.forEach(botao => {

    botao.addEventListener("click", () => {

        pontoId.value =
        botao.dataset.id

        nomePonto.value =
        botao.dataset.nome

        enderecoPonto.value =
        botao.dataset.endereco

        materiaisPonto.value =
        botao.dataset.materiais

        horarioPonto.value =
        botao.dataset.horario

        modalEditar.style.display =
        "flex"

    })

})

// =========================
// FECHAR MODAL EDITAR
// =========================

btnFecharEditar.addEventListener(
    "click",
    () => {

        modalEditar.style.display =
        "none"

    }
)

// =========================
// FECHAR CLICANDO FORA
// =========================

modalEditar.addEventListener(
    "click",
    (event) => {

        if (
            event.target === modalEditar
        ) {

            modalEditar.style.display =
            "none"

        }

    }
)


// =========================
// MODAL CADASTRAR PONTO
// =========================

const modalCadastro =
document.getElementById(
    "modal-cadastro"
)

const abrirCadastro =
document.getElementById(
    "abrir-modal-cadastro"
)

const btnFecharCadastro =
document.getElementById(
    "fechar-modal-cadastro"
)

// =========================
// ABRIR MODAL CADASTRO
// =========================

abrirCadastro.addEventListener(
    "click",
    () => {

        modalCadastro.style.display =
        "flex"
        console.log("JS carregado com sdfucesso")

    }
)

// =========================
// FECHAR MODAL CADASTRO
// =========================

btnFecharCadastro.addEventListener(
    "click",
    () => {

        modalCadastro.style.display =
        "none"

    }
)

// =========================
// FECHAR CLICANDO FORA
// =========================

modalCadastro.addEventListener(
    "click",
    (event) => {

        if (
            event.target === modalCadastro
        ) {

            modalCadastro.style.display =
            "none"

        }

    }
)

const botao = document.getElementById(
    "btn-localizacao"
)

botao.addEventListener("click", () => {

    navigator.geolocation.getCurrentPosition(

        (posicao) => {

            const latitude =
            posicao.coords.latitude

            const longitude =
            posicao.coords.longitude

            document.getElementById(
                "latitude"
            ).value = latitude

            document.getElementById(
                "longitude"
            ).value = longitude

            alert(
                "Localização capturada!"
            )

        },

        () => {

            alert(
                "Erro ao obter localização"
            )

        }

    )

})


