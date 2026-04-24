(function(){

    const loader = document.getElementById("marist-loader");
    const progressBar = document.querySelector(".loader-bar");
    const ajaxBar = document.getElementById("marist-ajax-bar");
    const mainContent = document.getElementById("main-content");

    /* ============================= */
    /* INITIAL PAGE LOAD            */
    /* ============================= */

    let progress = 0;

    function simulateProgress() {
        progress += 10;
        progressBar.style.width = progress + "%";

        if (progress < 90) {
            setTimeout(simulateProgress, 200);
        }
    }

    simulateProgress();

    window.addEventListener("load", function() {
        progressBar.style.width = "100%";

        setTimeout(() => {
            loader.classList.add("hidden");
            mainContent.setAttribute("aria-hidden", "false");
        }, 500);
    });

    /* ============================= */
    /* AJAX LOADER FUNCTION         */
    /* ============================= */

    window.maristLoadPage = function(url, targetId) {
        ajaxBar.style.width = "30%";

        fetch(url)
            .then(response => {
                ajaxBar.style.width = "70%";
                return response.text();
            })
            .then(data => {
                document.getElementById(targetId).innerHTML = data;
                ajaxBar.style.width = "100%";

                setTimeout(() => {
                    ajaxBar.style.width = "0%";
                }, 300);
            })
            .catch(() => {
                ajaxBar.style.width = "0%";
            });
    };

})();
