    
function show_settings(id) {
    const settings = document.getElementById(`show_settings_${id}`);
    
    settings.classList.toggle("hidden");
}

function expand_all_settings() {
    document.querySelectorAll('.setting').forEach( settingRow => {
        settingRow.classList.toggle("hidden");
    })
}

window.show_settings = show_settings
window.expand_all_settings = expand_all_settings
