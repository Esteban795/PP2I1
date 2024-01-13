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
        height = Math.max(maxItemsHeight, height)
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

const slides = document.querySelectorAll(".slide");
const nextSlideBtn = document.querySelector(".btn-next");
const prevSlideBtn = document.querySelector(".btn-prev");
let currSlide = 0;
let maxSlide = slides.length - 1;
  
updateSlides();

function updateSlides() {
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slides[currSlide].style.display = "block";  
}

function updateSlidersButtonsColors() {
    if (currSlide == 0) {
        nextSlideBtn.classList.add("svg-white");
        prevSlideBtn.classList.add("svg-white");
    } else {
        nextSlideBtn.classList.remove("svg-white");
        prevSlideBtn.classList.remove("svg-white");
    }
}
nextSlideBtn.addEventListener("click", function () {
        currSlide = (currSlide + 1) % (maxSlide + 1);
        updateSlidersButtonsColors();
        updateSlides();
    });

prevSlideBtn.addEventListener("click", function () {
    currSlide = currSlide == 0 ? maxSlide : currSlide - 1;
    updateSlidersButtonsColors();
    updateSlides();
});

const corner1 = L.latLng(-90, -180)
const corner2 = L.latLng(90, 180);
const bounds = L.latLngBounds(corner1, corner2);

var map = L.map('map',{minZoom: 2,maxBounds : bounds,maxBoundsViscosity: 1.0}).setView([51.505, -0.09],2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var bin_entries = document.getElementsByClassName("bin-entry");
for (var i = 0; i < bin_entries.length; i++) {
    bin_entries[i].addEventListener("click", function() {
        this.children[0].classList.toggle("displayed-bin");
        let lat = this.getAttribute("data-lat");
        let long = this.getAttribute("data-long");
        map.setView([lat, long], 8);
    });
    
}
