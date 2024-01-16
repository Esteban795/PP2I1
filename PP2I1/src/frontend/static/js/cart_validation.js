const allSameAdressCheckbox = document.querySelector('#all-same-adress');
const adressesInputs = document.querySelectorAll('.adress-input');

allSameAdressCheckbox.addEventListener('change', () => {
	if (allSameAdressCheckbox.checked) {
		adressesInputs.forEach(input => {
			input.disabled = true;
		});
		adressesInputs[0].disabled = false;
	} else {
		adressesInputs.forEach(input => {
			input.disabled = false;
		});
	}
});

adressesInputs.forEach(input => {
	input.addEventListener('input', () => {
		if (allSameAdressCheckbox.checked) {
			adressesInputs.forEach(a => {
				a.value = input.value;
			});
		}
	});
});