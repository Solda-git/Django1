'use strict'

window.onload = () => {
    console.log("DOM loaded");
    document.querySelectorAll('.minus')
        .forEach(item => {
            item.addEventListener("click", event => {
                console.log(event.target);


            });
        });
}

function hideCart() {
    let el = document.querySelector('.cart-block');
    if (el.classList.contains("invisible")) {
        el.classList.remove("invisible")
    }
    else {
        el.classList.add("invisible");
    }
}