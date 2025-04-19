document.addEventListener('DOMContentLoaded', function() {
    // Function to scroll to section if hash exists in URL
    function scrollToSection() {
        if (window.location.hash) {
            const targetId = window.location.hash.substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                setTimeout(() => {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }, 100);
            }
        }
    }

    // Scroll on page load if there's a hash
    scrollToSection();

    // Handle clicks on hash links when already on home page
    if (window.location.pathname === '/' || window.location.pathname === '/home/') {
        document.querySelectorAll('a[href*="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href.includes('#')) {
                    const targetId = href.split('#')[1];
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        window.scrollTo({
                            top: targetElement.offsetTop - 100,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }
}); 