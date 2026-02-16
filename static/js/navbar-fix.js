// Fix for navbarColorOnResize error - Check if element exists before accessing
(function() {
    'use strict';
    
    // Override the navbarColorOnResize function to add null check
    window.navbarColorOnResize = function() {
        let referenceButtons = document.querySelector("[data-class]");
        if (!referenceButtons) {
            // Element doesn't exist, skip this functionality
            return;
        }
        
        let sidenav = document.querySelector('.sidenav');
        if (!sidenav) {
            return;
        }
        
        if (window.innerWidth > 1200) {
            if (referenceButtons.classList.contains("active") && 
                referenceButtons.getAttribute("data-class") === "bg-transparent") {
                sidenav.classList.remove("bg-white");
            } else {
                sidenav.classList.add("bg-white");
            }
        } else {
            sidenav.classList.add("bg-white");
            sidenav.classList.remove("bg-transparent");
        }
    };
})();
