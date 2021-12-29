window.onload = () => {
    let alerts = document.querySelectorAll('#alert');

    function hideAlert(alert) {
        alert.style.animation = 'HideToTheRight 0.5s ease 0s forwards';
    }

    alerts.forEach(alert => {
        alert.addEventListener('click', () => {
            hideAlert(alert);
        });

        setTimeout(() => {
            hideAlert(alert);
         }, 7000);
    });
};
