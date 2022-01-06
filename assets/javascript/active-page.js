window.addEventListener('load', () => { 
    const path = window.location.pathname;

    if ( /job\/\d+\/edit/.test(path) ) {
        document.getElementById('job_edit_link').style.display = 'flex';
    } else if ( /job\/\d+$/.test(path) ) {
        document.getElementById('job_preview_link').style.display = 'flex';
    }
})