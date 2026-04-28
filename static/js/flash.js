document.addEventListener("DOMContentLoaded", function () {
    const flash = document.getElementById("flash-container");

    if (flash) {
        setTimeout(() => {
            flash.style.opacity = "0";

            setTimeout(() => {
                flash.remove();
            }, 500);

        }, 3000); // 3 segundos
    }
});