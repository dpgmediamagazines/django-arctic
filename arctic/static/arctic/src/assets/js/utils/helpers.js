//TODO: nest these helpers within one object, like arctic..

// global var whichs all public data, helpers etc..
window.arctic = {};
window.arctic.utils = {};


function slugify( Text ) {
    return Text
        .toLowerCase()
        .replace( /[^\w ]+/g, '' )
        .replace( / +/g, '-' );
}

// getCookie helper
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}