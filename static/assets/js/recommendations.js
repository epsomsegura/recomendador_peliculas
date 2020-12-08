$(document).ready(function () {
    var items = $(".card-item");

    var numItems = items.length;
    var perPage = 12;
    items.slice(perPage).hide();

    $('.pagination').pagination({
        items: numItems,
        itemsOnPage: perPage,
        cssStyle: 'light-theme',
        onPageClick: function (pageNumber) {
            var showFrom = perPage * (pageNumber - 1);
            var showTo = showFrom + perPage;
            items.hide().slice(showFrom, showTo).show();
        },
        prevText: 'Anterior',
        nextText: 'Siguiente',
    });
});