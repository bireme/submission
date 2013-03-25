// interface
function change_order_by(order) {
    var form = document.interface;
    form.order_by.value = order;
    form.submit();
}

function change_order_type(order) {
    var form = document.interface;
    if (form.order_type.value != "") {
        form.order_type.value = "";
    } else {
        form.order_type.value = "-";
    }
    form.submit();
}

function change_filter(filter) {
    var form = document.interface;
    form.filter.value = filter;
    form.page.value = 1;
    form.submit();
}

function change_type(type) {
    var form = document.interface;
    form.filtr_type.value = type;
    form.page.value = 1;
    form.submit();
}

function change_page(page) {
    var form = document.interface;
    form.page.value = page;
    form.submit();
}

// submissions
function toggle_all(obj) {
    if(obj.checked) {
        $(".checkbox_submission").attr('checked', true);
    } else {
        $(".checkbox_submission").attr('checked', false);
    }
}

function submission_action(action) {
    var form = document.submissions;
    var msg = "{% trans 'Do you really change this submission status?' %}";

    form.action.value = action;

    if(confirm(msg)) {
        form.submit();
    }
}