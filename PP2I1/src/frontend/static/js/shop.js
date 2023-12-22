var cartItems = [];
const cartDiv = document.getElementById("cart_list");
const formValidation = document.getElementById("validation-cart-form");
const cartConfirmButton = document.getElementById("cartConfirmButton");
const cartInput = document.getElementById("cart");
let ids_list = [];

function addToCart(item) {
    cartItems.push(item);
    ids_list.push(item.product_id);
    updateCart();
}

function updateCart() {
    console.log(ids_list);
    cartDiv.innerHTML = '';
    if (cartItems.length == 0) {
        cartDiv.innerHTML = '<li id="emptyCart">Vide actuellement</li>';
    }
    else {
        for (var i = 0; i < cartItems.length; i++) {
            var itemLi = document.createElement('li');
            var img = document.createElement('img');
            img.src = cartItems[i].img_src;
            img.style.width = '50px';
            img.style.height = '50px';
            itemLi.appendChild(img);
            var textNode = document.createTextNode(cartItems[i].name + ' - ' + cartItems[i].price);
            itemLi.appendChild(textNode);
            
            var removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.className = 'removeButton';
            removeButton.onclick = function() { removeFromCart(i); };
            itemLi.appendChild(removeButton);
            
            cartDiv.appendChild(itemLi);
        }

    }
}

function removeFromCart(index) {
    var index = cartItems.indexOf(index);
    ids_list.splice(index, 1);
    cartItems.splice(index, 1);
    updateCart();
}

const allSameAdressCheckbox = document.querySelector('#all-same-adress');
const adressesInputs = document.querySelectorAll('.adress-input');

allSameAdressCheckbox.addEventListener('change', () => {
    if (allSameAdressCheckbox.checked) {
        adressesInputs.forEach(input => {
            input.disabled = true;
        });
        adressesInputs[0].disabled = false;
    }
    else {
        adressesInputs.forEach(input => {
            input.disabled = false;
        });
    }
}
);

adressesInputs.forEach(input => {
    input.addEventListener('input', () => {
        if (allSameAdressCheckbox.checked) {
            adressesInputs.forEach(a => {
                a.value = input.value;
        }
        );
    }
    }
        );
    });