const statsItems = document.querySelectorAll('.item');
const maxItemsHeight = 400;
const initialItemsHeight = 100;


statsItems.forEach((item) => {

    item.addEventListener("mouseover", () => {
        let value = parseFloat(item.getAttribute('data-value'));
        let max = parseFloat(item.getAttribute('data-max-value'));
        let ratio = value / max;
        let height = Math.max(maxItemsHeight * ratio,initialItemsHeight);
        item.style.height = height + "px";
        item.classList.add("item-active");
    });
});

statsItems.forEach((item) => {
    item.addEventListener("mouseout", () => {
        item.style.height = initialItemsHeight + "px";
        item.classList.remove("item-active");
    });
});