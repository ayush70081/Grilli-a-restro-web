document.addEventListener('DOMContentLoaded', function() {
    // Category switching functionality
    const menuCategories = document.querySelectorAll('.menu-category');
    const menuSections = document.querySelectorAll('.menu-section');

    menuCategories.forEach(category => {
        category.addEventListener('click', function() {
            // Remove active class from all categories and sections
            menuCategories.forEach(cat => cat.classList.remove('active'));
            menuSections.forEach(section => section.classList.remove('active'));

            // Add active class to clicked category and corresponding section
            this.classList.add('active');
            const targetSection = document.querySelector(`.menu-section[data-category="${this.dataset.category}"]`);
            targetSection.classList.add('active');
        });
    });

    // Initialize view more buttons
    const viewMoreButtons = document.querySelectorAll('.view-more-btn');
    
    viewMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const menuSection = this.closest('.menu-section');
            const menuContainer = menuSection.querySelector('.menu-items-container');
            
            menuContainer.classList.toggle('expanded');
            this.classList.toggle('active');
            
            // Update button text based on state
            if (menuContainer.classList.contains('expanded')) {
                this.textContent = 'Show Less';
            } else {
                this.textContent = 'Show All Items';
            }
            
            if (!menuContainer.classList.contains('expanded')) {
                menuSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Hide View More button if section has 3 or fewer items
    document.querySelectorAll('.menu-section').forEach(section => {
        const items = section.querySelectorAll('.menu-item');
        const viewMoreBtn = section.querySelector('.view-more-btn');
        if (items.length <= 3 && viewMoreBtn) {
            viewMoreBtn.style.display = 'none';
        }
    });

    // Add intersection observer for animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all menu items
    document.querySelectorAll('.menu-item').forEach(item => {
        observer.observe(item);
    });
}); 