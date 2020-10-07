var selected_movies = [];

$(document).ready(function () {
    $('#tbl_movies').DataTable({
        "order": [[ 1, "desc" ]],
        'language': {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        }
    });
});

$(document).on('click', '[name="title"]', function () {
    var id = $(this).data('id');
    if ($(this).is(':checked')) {
        var obj = {
            id: $(this).data('id'),
            title: $(this).data('title')
        };
        selected_movies.push(obj);
    }
    else {
        selected_movies = $.grep(selected_movies, function (e) {
            return e.id !== id;
        });
    }

    var badges = '';

    $.each(selected_movies, function (i, val) {
        badges += '<span class="badge badge-secondary text-capitalize">' + val.title + ' <span class="badge badge-light delete-title" data-id="' + val.id + '" data-title="' + val.title + '">x</span></span> ';
    });

    $('#badges_titles').html(badges);

    $('#btn_show_modal').prop('disabled', (selected_movies > 0));
});

$(document).on('click', '.delete-title', function () {
    var id = $(this).data('id');
    $('#tbl_movies').DataTable().$('#' + id).prop('checked', false);
    selected_movies = $.grep(selected_movies, function (e) {
        return e.id !== id;
    });

    var badges = '';

    $.each(selected_movies, function (i, val) {
        badges += '<span class="badge badge-secondary text-capitalize">' + val.title + ' <span class="badge badge-light delete-title" data-id="' + val.id + '" data-title="' + val.title + '">x</span></span> ';
    });

    $('#badges_titles').html(badges);

    $('#btn_show_modal').prop('disabled', (selected_movies > 0));
});



$(document).on('click', '#btn_show_modal', function () {
    frmElements = '';
    $.each(selected_movies, function (i, val) {
        frmElements += '<div class="row">'
            + '<div class="col-12 col-sm-6">'
            + '<input type="hidden" name="title" value="' + val.title + '" >'
            + '<strong>' + val.title + '</strong>'
            + '</div>'

            + '<div class="col-12 col-sm-4">'
            + '<input type="range" name="rating" class="form-control rate" min="0" max="5" step="0.1" id="rate_' + i + '" value="0">'
            + '</div>'

            + '<div class="col-12 col-sm-2">'
            + '<span>Calificación: <strong id="val_rate_' + i + '">0.0</strong></span>'
            + '</div>'

            + '</div>';
    });

    $('#rating_form').html(frmElements);

    $.each($('.rate'), function (i, val) {
        var id = $(this).attr(id);
        var val = $(this).val();
        $('#val_' + id).html(val);
    });
});

$(document).on('change', '.rate', function () {
    var id = $(this).attr('id');
    var val = $(this).val();
    $('#val_' + id).html(val);
});

$(document).on('click', '#btn_send_data', function () {
    $('#rating_form').submit();
});