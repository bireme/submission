function check_all(attr) {
    fields = $("." + attr)
    fields.attr('checked', 'checked')
}
function show_options() {
    $(".options").toggle();
}
function output(attr) {
    var form = document.q
    form.output.value = attr
    form.submit()
}

$(function(){
    $("#searchButton").click(function(){
        var form = document.q
        form.output.value = "screen"
    });
});