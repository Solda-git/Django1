'use strict'

window.onload = () => {
    console.log("DOM loaded");
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