document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500); // Wait for fade out transition
        }, 5000);

        // Handle dismiss button click
        const dismissBtn = alert.querySelector('.alert-dismiss');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', () => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            });
        }
    });
});
