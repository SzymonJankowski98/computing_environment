window.addEventListener('load', () => {
    let field = document.getElementById("id_language");
    if (!field) return;

    field.addEventListener('change', () => {
        let pythonHelper = document.getElementById("python-helper");
        let javaHelper = document.getElementById("java-helper");
        pythonHelper.classList.toggle("hidden");
        javaHelper.classList.toggle("hidden");
    })

});