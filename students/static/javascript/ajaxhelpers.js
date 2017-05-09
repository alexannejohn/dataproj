var getCookie = function(name) {
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
};

var setCSRF = function() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        }
    });
};
// set the CSRF token necessary for patch requests
setCSRF();

// CSRF tokens are needed in like 3 different places. it's very annoying
var InitializeForm = function(){
    var csrftoken = getCookie('csrftoken');
    var form = new FormData();
    form.append("csrfmiddlewaretoken", csrftoken);
    return form;
};

var getPostSettings = function(url, data){
    var settings = {
          "async": true,
          "crossDomain": true,
          "url": url,
          "method": "POST",
          "headers": {
            "cache-control": "no-cache",
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": data
        };
    return settings;
};

var getPatchSettings = function(url, data){
    var settings = {
          "async": true,
          "crossDomain": true,
          "url": url,
          "method": "PATCH",
          "headers": {
            "cache-control": "no-cache",
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": data
        }
    return settings;
};
