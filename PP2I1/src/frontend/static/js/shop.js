var cartItems = [];

function addToCart(item) {
    cartItems.push(item);
    updateCart();
}

function updateCart() {
    var cartDiv = document.getElementById("cart_list");
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
    cartItems.splice(index, 1);
    updateCart();
}