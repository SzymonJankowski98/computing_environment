window.addEventListener('load', () => {
    if (window.location.pathname == '/dashboard'){
        document.getElementById("sort-button").onclick = changeButtonImg
    }

    function changeButtonImg(){
        let sort_img = document.getElementById("sort-button-img");
        let order = document.getElementById("id_order");

        if (order.value == '') {
            sort_img.src = '../static/ascending-sort.svg';
            order.value = '-';

        } else {
            sort_img.src = '../static/descending-sort.svg';
            order.value = '';

        }
    }

    let sort_img = document.getElementById("sort-button-img");
    let order = document.getElementById("id_order");

    if (order.value == '') {
        sort_img.src = '../static/descending-sort.svg';
    } else {
        sort_img.src = '../static/ascending-sort.svg';
    }

})
