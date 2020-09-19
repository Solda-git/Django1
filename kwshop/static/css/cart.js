'use strict'

window.onload = () => {
    console.log("DOM loaded");
    alert('From script');

}

function hideCart() {
    el = document.querySelector('.cart-block');
    if (el.classList.contains("invisible")) {
        el.classList.remove("invisible")
    }
    else {
        el.classList.add("invisible");
    }
}