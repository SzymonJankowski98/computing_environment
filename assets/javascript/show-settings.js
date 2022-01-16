    
function show_settings(id) {
    const settings = document.getElementById(`show_settings_${id}`);
    
    settings.classList.toggle("hidden");
}

window.show_settings = show_settings