document.addEventListener("DOMContentLoaded", function () {

    const slides = document.querySelectorAll('.slide');
    const slider = document.getElementById('slider');

    let index = 0;
    let interval = setInterval(nextSlide, 5000);

    function nextSlide() {
        slides[index].classList.remove('active');
        index = (index + 1) % slides.length;
        slides[index].classList.add('active');
    }

    // Pause on hover
    slider.addEventListener("mouseenter", () => {
        clearInterval(interval);
    });

    slider.addEventListener("mouseleave", () => {
        interval = setInterval(nextSlide, 5000);
    });

});
