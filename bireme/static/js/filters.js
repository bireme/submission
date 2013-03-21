$(function(){

    // escondendo filters
    $('#filtersPanel').css('right', '-240px');

    var speed = 250;
    var button = $("#filtersPanel");
    button.hover(function(){
        // se ja tiver totalmente aberto, fecha denovo
        if($('#filtersPanel').css('right') == '0px') {
            $('#filtersPanel').animate({right: '-240px',}, speed, function(){});
           
        } 
        // se ja tiver totalmente fehcado, abre denovo
        if($('#filtersPanel').css('right') == '-240px') {
            $('#filtersPanel').animate({right: '0px',}, speed, function(){});

        }
    });
});