window.onload = () => {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const progress = parseFloat(bar.dataset.progress);
        if (isNaN(progress)) return;

        if (progress > 85) {
            bar.style.background = '#f87171';
        } else if (progress > 70) {
            bar.style.background = '#fdba74';
        } else if (progress > 50) {
            bar.style.background = '#fcd34d';
        } else {
            bar.style.background = '#86efac';
        };

        bar.style.width = `${Math.round(progress)}%`;
        console.log(bar)
    });
};
