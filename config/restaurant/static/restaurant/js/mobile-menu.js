document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navList = document.querySelector('.nav-list');
    
    if (menuToggle && navList) {
        menuToggle.addEventListener('click', function() {
            navList.classList.toggle('active');
            this.textContent = navList.classList.contains('active') ? '✕' : '☰';
            
            // Prevent body scrolling when menu is open
            document.body.style.overflow = navList.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navList.classList.remove('active');
                menuToggle.textContent = '☰';
                document.body.style.overflow = '';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navList.contains(event.target) || menuToggle.contains(event.target);
            if (!isClickInside && navList.classList.contains('active')) {
                navList.classList.remove('active');
                menuToggle.textContent = '☰';
                document.body.style.overflow = '';
            }
        });
    }
}); 