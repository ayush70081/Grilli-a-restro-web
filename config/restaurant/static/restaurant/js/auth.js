document.addEventListener('DOMContentLoaded', function() {
    // Get modal elements
    const authModal = document.getElementById('authModal');
    const loginContainer = document.getElementById('loginContainer');
    const signupContainer = document.getElementById('signupContainer');
    const loginLink = document.getElementById('loginLink');
    const authClose = document.getElementById('authClose');
    const goToSignup = document.getElementById('goToSignup');
    const goToLogin = document.getElementById('goToLogin');

    // Show modal when login link is clicked
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            authModal.classList.add('active');
            loginContainer.style.display = 'flex';
            signupContainer.style.display = 'none';
        });
    }

    // Close modal when close button is clicked
    if (authClose) {
        authClose.addEventListener('click', function() {
            authModal.classList.remove('active');
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === authModal) {
            authModal.classList.remove('active');
        }
    });

    // Toggle between login and signup
    if (goToSignup) {
        goToSignup.addEventListener('click', function() {
            loginContainer.style.display = 'none';
            signupContainer.style.display = 'flex';
        });
    }

    if (goToLogin) {
        goToLogin.addEventListener('click', function() {
            signupContainer.style.display = 'none';
            loginContainer.style.display = 'flex';
        });
    }
}); 