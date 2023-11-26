const slides = document.querySelectorAll(".slide");
const nextSlideBtn = document.querySelector(".btn-next");
const prevSlideBtn = document.querySelector(".btn-prev");
let currSlide = 0;
let maxSlide = slides.length - 1;

// loop through slides and set each slides translateX property to index * 100% 
slides.forEach((slide, indx) => {
  slide.style.transform = `translateX(${indx * 100}%)`;
});


nextSlideBtn.addEventListener("click", function () {
    currSlide = (currSlide + 1) % (maxSlide + 1);
    slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - currSlide)}%)`;
  });
});

prevSlideBtn.addEventListener("click", function () {
    currSlide = (currSlide === 0) ? maxSlide : currSlide - 1;
    slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - currSlide)}%)`;
  });
});