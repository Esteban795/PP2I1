const filterOptionsSelect = document.getElementById("filter-options");

let filterOptionTDIndex = new Map([
	['Plus récent', 1],
	['Plus ancien', -1],
	['Prix croissant', -4],
	['Prix décroissant', 4],
]);

function parseDate(d) {
	let temp = Date.parse(d);
	return temp;
}

function parsePrice(p) {
	return parseInt(p.slice(0, -1));
}

filterOptionsSelect.addEventListener('change', (e) => {
	const filterOption = e.target.value;
	let filterIndex = filterOptionTDIndex.get(filterOption);
	let absIndex = Math.abs(filterIndex);
	let tbody = purchaseHistoryTable.querySelector('tbody');
	let rows = [].slice.call(tbody.querySelectorAll('tr'));
	parser_used = absIndex == 1 ? parseDate : parsePrice;
	rows.sort(function (a, b) {
		let res = parser_used(b.children[absIndex - 1].innerHTML) - parser_used(a.children[absIndex - 1].innerHTML);
		return res;
	});
	if (filterIndex < 0) {
		rows.reverse();
	}
	tbody.replaceChildren()
	for (let i = 0; i < rows.length; i++) {
		tbody.appendChild(rows[i]);
	}
});

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
			if (cell.classList.contains('column-hidden')) continue;
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
	['date', 0],
	['client-name', 1],
	['email', 2],
	['price', 3],
	['actions', 4]
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
		if (!event.target.checked) {
			for (let i = 0; i < tableRows.length; i++) {
				tableRows[i].children[index].classList.add('column-hidden');
			}
		} else {
			for (let i = 0; i < tableRows.length; i++) {
				tableRows[i].children[index].classList.remove('column-hidden');
			}
		}
	});
});


const resultCountSelect = document.querySelector("#number-of-results-select");

resultCountSelect.addEventListener('change', (e) => {
	const resultCount = e.target.value;
	let trs = purchaseHistoryTable.querySelectorAll('tr');
	if (resultCount == 'all') {
		for (let i = 1; i < trs.length; i++) {
			trs[i].classList.remove('hidden');
		}
		return;
	}
	for (let i = 1; i < trs.length; i++) {
		const element = trs[i];
		if (i <= resultCount) {
			element.classList.remove('hidden');
		} else {
			element.classList.add('hidden');
		}
	}
});

const openDialogsButtons = document.querySelectorAll('.open-dialog-button');
const closeDialogsButtons = document.querySelectorAll('.close-dialog-button');

openDialogsButtons.forEach((button) => {
	button.addEventListener('click', (event) => {
		event.target.previousElementSibling.showModal();
	});
});

closeDialogsButtons.forEach((button) => {
	button.addEventListener('click', (event) => {
		event.target.parentElement.close();
	});
});

const transactionProductEntries = document.querySelectorAll('.transaction-product-entry');
const dialogForm = document.querySelector('#dialog-form');

transactionProductEntries.forEach((entry) => {
	entry.addEventListener('click', () => {
		transactionProductEntries.forEach((entry) => {
			entry.style.display = 'none';
		});
		entry.style.display = '';
		entry.parentElement.lastElementChild.style.display = 'block';
		let product_id = entry.getAttribute('data-product-id');
		dialogForm.action = `/admin/add-transaction/${product_id}`;
	});
});

const transactionCancelProductSelection = document.querySelectorAll('.transaction-cancel-product-selection');

transactionCancelProductSelection.forEach((button) => {
	button.addEventListener('click', (event) => {
		event.target.parentElement.parentElement.style.display = 'none';
		transactionProductEntries.forEach((entry) => {
			entry.style.display = '';
		});
	});
});


const userRows = document.querySelectorAll('.user-row');
const adminOnlyCheckbox = document.querySelector('#admin-only-checkbox');

adminOnlyCheckbox.addEventListener('change', (event) => {
	if (event.target.checked) {
		userRows.forEach((row) => {
			if (!row.classList.contains('admin')) {
				row.classList.add('hidden');
			}
		});
	} else {
		userRows.forEach((row) => {
			row.classList.remove('hidden');
		});
	}
});