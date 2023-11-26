const productsOptions = document.querySelectorAll('.management-option');
const div2 = document.querySelector('.div2');
const div3 = document.querySelector('.div3');

const div2Children = div2.children;
const div3Children = div3.children;
let SELECTED_OPTION = false;

productsOptions.forEach((option) => {
    option.addEventListener('click', () => {
        for (let i = 0; i < productsOptions.length; i++) {
            productsOptions[i].classList.remove('selected-option');
        }
        option.classList.add('selected-option');

        let id = parseInt(option.getAttribute('data-id'));
        var firstOtherNumber = (id + 1) % 3;
        var secondOtherNumber = (id + 2) % 3;

        div2Children[id].classList.remove('hidden');
        div3Children[id].classList.remove('hidden');

        div2Children[firstOtherNumber].classList.add('hidden');
        div3Children[firstOtherNumber].classList.add('hidden');

        div2Children[secondOtherNumber].classList.add('hidden');
        div3Children[secondOtherNumber].classList.add('hidden');
  });
}
);

const productsEntriesContainers = document.querySelectorAll('.product-entry-container');
const productsEntries = document.querySelectorAll('.product-entry');
const modifyInputs = document.querySelectorAll('.modify-input');
const addInputs = document.querySelectorAll('.add-input');
const cancelSelectionBtns = document.querySelectorAll('.cancel-selection');
const addPreview = document.querySelector('.preview');

productsEntries.forEach((entry) => {
    entry.addEventListener('click', () => {
        SELECTED_OPTION = true;
        let infos = entry.querySelectorAll('p');
        productsEntriesContainers.forEach((temp) => {
            temp.classList.add('hidden');
        });
        entry.parentElement.classList.remove('hidden');
        entry.parentElement.children[1].classList.remove('hidden');
        for (let i = 0; i < infos.length; i++) {
            modifyInputs[i].value = infos[i].innerHTML;
        }
    });
}
);

cancelSelectionBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        for (let i = 0; i < productsEntriesContainers.length; i++) {
            productsEntriesContainers[i].classList.remove('hidden'); 
        }
        btn.classList.add('hidden');
        SELECTED_OPTION = false;
    });
}
);

function getSelectedProductContainer() {
    for (let i = 0; i < productsEntriesContainers.length; i++) {
        if (!productsEntriesContainers[i].classList.contains('hidden')) {
            return productsEntriesContainers[i];
        }
    }
};

modifyInputs.forEach((input) => {
    input.addEventListener('input', () => {
        if (!SELECTED_OPTION) return;
        let selectedProductContainer = getSelectedProductContainer();
        let selectedProductInfos = selectedProductContainer.children[0].children[1];
        for (let i = 0; i < selectedProductInfos.children.length; i++) {
            selectedProductInfos.children[i].innerHTML = modifyInputs[i].value;
        }
    });
}
);

addInputs.forEach((input) => {
    input.addEventListener('input', () => {
        let fields = addPreview.querySelectorAll('.fields');
        console.log(fields)
    });
}
);


const previewImage = (event) => {
    let selectedProductContainer = getSelectedProductContainer();
    const imagePreviewElement = selectedProductContainer.querySelector(".product-entry-img").children[0];
    imagePreviewElement.src = URL.createObjectURL(event.target.files[0]);
};