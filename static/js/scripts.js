document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alertElement) => {
        setTimeout(() => {
            alertElement.classList.add('fade');
            alertElement.classList.remove('show');
        }, 4000);
    });
});
