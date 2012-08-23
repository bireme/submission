$(function(){
    // listen action button clicks
    $('.actions .btn').click(function(){
        var obj = $(this);
        change_status(obj.attr('action'));
    });
});

// happens when has click on pending/decline/next step button
function change_status(action) {
    var form = document.change_status;
    form.action.value = action;
}