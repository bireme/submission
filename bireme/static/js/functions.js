// open follow up from submission in show.html
function open_message(id_message) {
    $(id_message).toggle('fast');
}

// change language
function change_language(lang) {
    
    // chama, via ajax, a view que armazena a linguagem em cookie, para relembrar na proxima entrada
    $.get("{% url main.views.cookie_lang %}", { language: lang} , function(data) {
        
        var form = document.language;
        form.language.value = lang;
        form.submit();
    });

    }