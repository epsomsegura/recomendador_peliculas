var selected_categories = [];

$(document).ready(function () {
    var items = $(".card-item");

    var numItems = items.length;
    var perPage = 6;
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
        hrefTextPrefix: '#pagina_'
    });
});

$(document).on('click', '[name="categoria"]', function () {
    if ($(this).is(':checked')) {
        selected_categories.push($(this).attr('id'));
    }
    else {
        var index = selected_categories.indexOf($(this).attr('id'));
        if (index > -1) {
            selected_categories.splice(index, 1)
        }
    }

    var badges = '';

    $.each(selected_categories, function (i, val) {
        badges += '<span class="badge badge-secondary text-capitalize">' + val + ' <span class="badge badge-light delete-category" data-id="' + val + '">x</span></span> ';
    });

    console.log(selected_categories);
    $('#badges_categories').html(badges);
});

$(document).on('click', '.delete-category', function () {
    var id = $(this).data('id');
    $('#' + id).prop('checked', false);
    var index = selected_categories.indexOf(id);
    if (index > -1) {
        selected_categories.splice(index, 1)
    }

    var badges = '';

    $.each(selected_categories, function (i, val) {
        badges += '<span class="badge badge-secondary text-capitalize">' + val + ' <span class="badge badge-light delete-category" data-id="' + val + '">x</span></span> ';
    });

    console.log(selected_categories);
    $('#badges_categories').html(badges);
});
