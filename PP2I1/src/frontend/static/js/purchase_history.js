// const filterOptionsSelect = document.querySelector("#filter-options-select");
// const manageColumnsSelect = document.querySelector("#manage-columns-select");
// const numberOfResultsSelect = document.querySelector("#number-of-results-select");

// let filterOptionTDIndex = new Map([
//     ['Plus récent',0],
//     ['Plus ancien',-0],
//     ['Prix croissant',1],
//     ['Prix décroissant',-1],
// ]);


// filterOptionsSelect.addEventListener('change', (e) => {
//     const filterOption = e.target.value;

// });


const searchbar = document.getElementById('search-bar');
const purchaseHistoryTable = document.getElementById('purchase-history-table');
const tableHeaders = document.getElementsByTagName("th");
const tableRows = purchaseHistoryTable.getElementsByTagName('tr');

searchbar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();
    let trs = purchaseHistoryTable.querySelectorAll('tr');
    for (let i = 1; i < trs.length; i++) {
        const element = trs[i];
        let found = false;
        for (let i = 0; i < element.children.length; i++) {
            const cell = element.children[i];
            if (cell.innerHTML.toLowerCase().includes(searchString)) {
                found = true;
                break;
            }
        }
        found ? element.classList.remove('hidden') : element.classList.add('hidden');
    }
});


let expanded = false;
const selectCheckboxes = document.querySelector("#checkboxes");
const columnsCheckboxes = document.querySelectorAll(".columns-checkboxes");

const columnsIndexes = new Map([
  ['date',0],
  ['client-name',1],
  ['email',2],
  ['price',3],
  ['actions',4]
]);

function showCheckboxes() {
  if (!expanded) {
    selectCheckboxes.style.display = "block";
    expanded = true;
  } else {
    selectCheckboxes.style.display = "none";
    expanded = false;
  }
}

columnsCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", (event) => {
    let index = columnsIndexes.get(event.target.value);
    console.log(index);
    if (!event.target.checked) {
        for (let i = 0; i < tableRows.length; i++){
            tableRows[i].children[index].classList.add('column-hidden');
        }
    } else {
        for (let i = 0; i < tableRows.length; i++){
            tableRows[i].children[index].classList.remove('column-hidden');
        }
    }
  });
});