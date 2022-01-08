window.onload = () => {
    const container  = document.getElementById('settings-editor');
    const form = document.getElementById('job-form');
    if (!container || !form) return;

    const options = {
        mode: 'code'
    }
    const editor = new JSONEditor(container, options)

    const settingsField = form.querySelector('.settings-field');
    if (!settingsField) return;
    if (settingsField.value) {
        try {
            editor.set(JSON.parse(settingsField.value));
        } catch (error) {
            console.log(error);
        }
    }

    document.querySelector('.jsoneditor-poweredBy').remove();

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        try {
            settingsField.value = JSON.stringify(editor.get());
            form.submit();
        } catch (error) {
            let settingsError = form.querySelector('#settings-error');
            settingsError.textContent = "Invalid JSON";
        }
    })
};