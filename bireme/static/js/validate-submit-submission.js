function check_iso_form() {
    form = document.iso;
    
    if (form.total_records.value == 0 || form.total_records.value == "") {
        alert(invalid_records_message);
        return false;
    }

    if (form.bibliographic_type.value === "") {
        alert(invalid_bibliographic_type_message);
        return false;
    }

    if (form.iso_file.value == "") {
        alert(invalid_iso_file_message);
        return false;
    }
}

$(function(){

    // allow only numbers in total_records
    $("#id_total_records").keydown(function(event) {
        // Allow: backspace, delete, tab, escape, and enter
        if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 || 
             // Allow: Ctrl+A
            (event.keyCode == 65 && event.ctrlKey === true) || 
             // Allow: home, end, left, right
            (event.keyCode >= 35 && event.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        else {
            // Ensure that it is a number and stop the keypress
            if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                event.preventDefault(); 
            }   
        }
    });

});