document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert-message');
    
    messages.forEach(message => {
        // Add fade out class after 3 seconds
        setTimeout(() => {
            message.classList.add('fade-out');
        }, 3000);

        // Remove the message from DOM after animation completes
        setTimeout(() => {
            message.remove();
        }, 3500);
    });
}); 