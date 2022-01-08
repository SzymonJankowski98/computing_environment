window.addEventListener('load', () => {
    let sort_button = document.getElementById("sort-button");
    let sort_img = document.getElementById("sort-button-img");
    let order = document.getElementById("id_order");

    if (!sort_button || !sort_img || !order) { return; }

    sort_button.onclick = changeButtonImg
    
    if (order.value == '') {
        sort_img.src = '../static/descending-sort.svg';

    } else {
        sort_img.src = '../static/ascending-sort.svg';
    }

    function changeButtonImg(){
        if (order.value == '') {
            sort_img.src = '../static/descending-sort.svg';
            order.value = '-';

        } else {
            sort_img.src = '../static/ascending-sort.svg';
            order.value = '';
        }
    }
})
