window.addEventListener('load', () => { 
    console.log(window.location.pathname);
    const path = window.location.pathname;

    if ( /job\/\d+\/edit/.test(path) ) {
        document.getElementById('job_edit_link').style.display = 'flex';
        console.log("Job Edit Page Here")
    } else if ( /job\/\d+$/.test(path) ) {
        document.getElementById('job_preview_link').style.display = 'flex';
        console.log("Job Preview Page Here")
    }

})