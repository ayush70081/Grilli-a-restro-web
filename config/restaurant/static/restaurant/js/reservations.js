function toggleDetails(card) {
    showBookingDetails(card);
}

function modifyReservation(id) {
    // Redirect to the modify reservation page
    window.location.href = `/modify-reservation/${id}/`;
}

function cancelReservation(id) {
    if (confirm('Are you sure you want to cancel this reservation?')) {
        // Get the CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Send POST request to cancel the reservation
        fetch(`/cancel-reservation/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                // Reload the page after successful cancellation
                window.location.reload();
            } else {
                alert('Failed to cancel reservation. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while cancelling the reservation.');
        });
    }
}

function showBookingDetails(card) {
    const modal = document.getElementById('bookingModal');
    
    // Get data from the card
    const reservationId = card.getAttribute('data-id');
    const name = card.getAttribute('data-name');
    const dateText = card.querySelector('.preview-item:nth-child(1) .detail-text').textContent;
    const timeText = card.querySelector('.preview-item:nth-child(2) .detail-text').textContent;
    const guestsText = card.querySelector('.preview-item:nth-child(3) .detail-text').textContent;
    const phone = card.getAttribute('data-phone');
    const requests = card.getAttribute('data-requests');
    const status = card.querySelector('.status-upcoming') ? 'upcoming' : 'past';

    // Update modal content
    document.getElementById('modalName').textContent = name;
    document.getElementById('modalDate').textContent = dateText;
    document.getElementById('modalTime').textContent = timeText;
    document.getElementById('modalGuests').textContent = guestsText;
    document.getElementById('modalPhone').textContent = phone;
    
    const requestsContainer = document.getElementById('specialRequestsContainer');
    if (requests && requests !== "None" && requests !== "") {
        document.getElementById('modalRequests').textContent = requests;
        requestsContainer.style.display = 'flex';
    } else {
        requestsContainer.style.display = 'none';
    }

    // Show/hide action buttons based on status
    const actionButtons = modal.querySelector('.modal-actions');
    if (status === 'upcoming') {
        actionButtons.style.display = 'flex';
        
        // Set up modify button
        const modifyBtn = actionButtons.querySelector('.btn-modify');
        modifyBtn.onclick = () => modifyReservation(reservationId);

        // Set up cancel button
        const cancelBtn = actionButtons.querySelector('.btn-cancel');
        cancelBtn.onclick = () => cancelReservation(reservationId);
    } else {
        actionButtons.style.display = 'none';
    }

    // Show modal
    modal.style.display = 'flex';
    setTimeout(() => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }, 10);
}

// Close modal when clicking outside or on close button
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('bookingModal');
    const closeBtn = modal.querySelector('.close-modal');

    closeBtn.onclick = function() {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }

    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }, 300);
        }
    }
}); 