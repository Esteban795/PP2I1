const allSameAdressCheckbox = document.querySelector('#all-same-adress');
const adressesInputs = document.querySelectorAll('.adress-input');
const adressesRegister = document.querySelector('#adresses-register');
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
    }}
    );
});

adressesInputs.forEach(input => {
    input.addEventListener('focusout', () => {
        
        let lst = adressesRegister.value.split('--');
        console.log(lst);
        let index = parseInt(input.getAttribute('data-item-index')) - 1;
        lst[index] = input.value;
        console.log(lst);
        adressesRegister.value = lst.join('--');
    }
    );
}
);

console.log()
