// Cookie Consent Banner — only appears for new visitors
window.addEventListener('DOMContentLoaded', function () {
    var banner = document.getElementById('cookieConsent');
    var acceptBtn = document.getElementById('acceptCookies');

    if (!banner || !acceptBtn) return; // Safety: elements must exist

    // Only show to visitors who have NOT yet accepted
    if (!localStorage.getItem('cookieAccepted')) {
        // Short delay so the page settles before the banner slides up
        setTimeout(function () {
            banner.classList.add('show');
        }, 1200);
    }

    acceptBtn.addEventListener('click', function () {
        localStorage.setItem('cookieAccepted', 'true');
        banner.classList.remove('show');
        // Completely hide after animation ends (0.55s)
        setTimeout(function () {
            banner.style.display = 'none';
        }, 600);
    });
});
