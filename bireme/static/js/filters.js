$(function(){

    $('#filtersPanel').css('right', '-240px');

    var speed = 500;
    var is_open = false;
    var button = $("#filtersPanel");
    button.hover(function(){
        if(is_open) {
            $('#filtersPanel').animate({right: '-240px',}, speed, function(){});
            is_open = false;
        } else {
            $('#filtersPanel').animate({right: '0px',}, speed, function(){});
            is_open = true;
        }
    });
});