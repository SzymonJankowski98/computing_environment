window.addEventListener('load', () => {
    document.getElementById("sort-button").onclick = changeButtonImg

    let init_img = true;

    function changeButtonImg(){
        let sort_img = document.getElementById("sort-button-img");

        init_img = !init_img;
        if (init_img) {
            sort_img.src = '../static/ascending-sort.svg';
        } else {
            sort_img.src = '../static/descending-sort.svg';
        }
    }
})