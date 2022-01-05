window.addEventListener('load', () => {
    let dashboardNav = document.getElementById('dashboard-nav');
    let hamburgerBtn = document.getElementById('dashboard-hamburger');

    if (!dashboardNav || !hamburgerBtn) return;

    hamburgerBtn.addEventListener('click', () => {
        dashboardNav.classList.toggle('hidden');
    });
});
