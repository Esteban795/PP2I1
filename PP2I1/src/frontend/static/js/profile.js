const statsItems = document.querySelectorAll('.item');
const maxItemsHeight = 400;
const initialItemsHeight = 100;

statsItems.forEach((item) => {
    item.addEventListener("mouseenter", () => {
        let statDescContainer = item.querySelector('.stat-desc-container');
        let statDescContainerHeight =  initialItemsHeight + statDescContainer.offsetHeight;
        let availableRange =  maxItemsHeight - statDescContainerHeight;
        let value = parseFloat(item.getAttribute('data-value'));
        let max = parseFloat(item.getAttribute('data-max-value'));
        let ratio = Math.min(1,value / max);
        let height = statDescContainerHeight + (availableRange * ratio);
        item.style.height = height + "px";
        item.classList.add("item-active");
    });
});

statsItems.forEach((item) => {
    item.addEventListener("mouseleave", () => {
        item.style.height = initialItemsHeight + "px";
        item.classList.remove("item-active");
    });
});

window.onload = function(){
    let h1FadeIn = document.querySelectorAll('.fadein-animation');
    for (let i = 0; i < h1FadeIn.length - 1; i++) {
      h1FadeIn[i].style.animationDelay = (i + 1) * 0.1 + 's';   
    }
  }