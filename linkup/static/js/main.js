document.querySelectorAll('.event-actions a').forEach(function(link) {
    if (link.textContent === 'Delete') {
        link.addEventListener('click', function(event) {
            const confirmation = confirm('Are you sure you want to delete this event?');
            if (!confirmation) {
                event.preventDefault();  // Prevent the default link behavior if not confirmed
            }
        });
    }
});
