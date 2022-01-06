window.addEventListener('load', () => {
    let order = document.getElementById("sort-button");
    let sort_img = document.getElementById("sort-button-img");

    if (order.value == '') {
        sort_img.src = '../static/descending-sort.svg';
        order.value = '-';
    } else {
        sort_img.src = '../static/ascending-sort.svg';
        order.value = '';
    }

})
