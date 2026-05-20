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