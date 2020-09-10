'use strict'

/*window.onload = () => {
    console.log("DOM loaded");
    document.querySelectorAll('.minus')
        .forEach(item => {
            item.addEventListener("click", event => {
                const request = new XMLHttpRequest();
                const url = `/cartbox/change/${event.currentTarget.getAttribute('item')}/quantity/${parseInt(event.currentTarget.getAttribute('quantity')) - 1}/`;
                console.log(url);
                fetch(url, {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    },
                })
                    .then(result => result.text())
                    .then(data =>  {
                        console.log("Data is ok", data);
                        document.getElementById('cart-box').innerHTML = data;
                    })
                    .catch(error => (console.log(error)));
            });
        });
}*/

666
window.onload = () => {
    console.log("DOM loaded");
    document.querySelectorAll('.minus')
        .forEach(item =>
            item.addEventListener("click", eventHandler)
            );
}

function eventHandler(event) {
    const request = new XMLHttpRequest();
    const url = `/cartbox/change/${event.currentTarget.getAttribute('item')}/quantity/${parseInt(event.currentTarget.getAttribute('quantity'))-1}/`;
    console.log(url);
    fetch(url,{
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "text/html"
        },
    })
        .then(result => result.text())
        .then(data => {
            document.getElementById("cart-box").innerHTML = data;
            document.querySelectorAll('.minus').forEach(item =>
                item.addEventListener("click", eventHandler));
            }
        )
        .catch(error => (console.log(error)));
}












function hideCart() {
    let el = document.querySelector('.cart-block');
    if (el.classList.contains("invisible")) {
        el.classList.remove("invisible")
    } else {
        el.classList.add("invisible");
    }
}