
$(document).ready(function(){
    $('#loader_container').fadeOut(1000);
});

$(document).on('submit','form',function(){
    $('#loader_container').show();
});