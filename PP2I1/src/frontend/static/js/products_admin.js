const productsOptions = document.querySelectorAll('.management-option');
const optionTitle = document.querySelector('#option-title');
const div2 = document.querySelector('.div2');
const div3 = document.querySelector('.div3');
const previewAddProduct = document.querySelector("#add-preview");
const formEndpoint = document.getElementById("form-products");

let MODE = "add";
let SELECTED_CONTAINER = previewAddProduct;

productsOptions.forEach((option) => {
    option.addEventListener('click', () => {
        for (let i = 0; i < productsOptions.length; i++) {
            productsOptions[i].classList.remove('selected-option');
        }
        option.classList.add('selected-option');
        let id = parseInt(option.getAttribute('data-id'));
        MODE = id === 0 ? "add" : "modify";
        if (MODE === "add") {
            optionTitle.textContent = 'Ajouter un produit';
            SELECTED_CONTAINER
            SELECTED_CONTAINER = previewAddProduct;
            previewAddProduct.style.display = 'flex';
            formEndpoint.action = "/admin/add-product";
        } else {
            optionTitle.textContent = 'Modifier un produit';
            SELECTED_CONTAINER = null;
            previewAddProduct.style.display = 'none';
        }
        let other = 1 - id;
        div3.children[id].classList.remove('hidden');
        div3.children[other].classList.add('hidden');
  });
}
);

const formInputs = document.querySelectorAll('.input');
const productsEntriesContainers = document.querySelectorAll('.product-entry-container');
const productsEntries = document.querySelectorAll('.product-entry');
const cancelSelections = document.querySelectorAll('.cancel-selection');
const findIndex = new Map([['product-name', 0], ['price',3], ['desc', 2], ['volume',1], ['stock', 4]]);

productsEntries.forEach((entry) => {
    entry.addEventListener('click', () => {
        if (MODE === 'add') return;
        SELECTED_CONTAINER = entry.parentElement;
        productsEntriesContainers.forEach((container) => {
            container.style.display = 'none';
        }
        );
        SELECTED_CONTAINER.style.display = 'flex';
        SELECTED_CONTAINER.children[1].style.display = 'flex';
        let product_id = entry.getAttribute('data-id');
        formEndpoint.action = "/admin/modify-product/" + product_id;
    });
}
);

cancelSelections.forEach((cancel) => {
    cancel.addEventListener('click', () => {
        cancel.parentElement.parentElement.style.display = 'none';
        productsEntriesContainers.forEach((container) => {
            container.style.display = 'flex';
        }
        );
        SELECTED_CONTAINER = null;
        formEndpoint.action = "/admin/modify-product/";
    });
}
);

formInputs.forEach((input) => {
    input.addEventListener('input', () => {
        let fields = SELECTED_CONTAINER.querySelectorAll('.fields');
        let inputName = input.name;
        let index = findIndex.get(inputName);
        fields[index].innerHTML = input.value;
    });
}
);


const previewImage = (event) => {
    const imagePreviewElement = SELECTED_CONTAINER.querySelector(".product-entry-img").children[0];
    imagePreviewElement.src = URL.createObjectURL(event.target.files[0]);
};