$(document).ready(function(){
    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
    });
    $('DIV.subUnsubButtons BUTTON').on('click', function(){
        var userId = $(this).data('userid')
        console.log($(this).attr('class'))
        if ($(this).attr('class') == 'subscribeButton'){
            var url = '/Subscribe'
            var self = this
            var data = {
                'userId': userId,
            }
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function() {
                    $(self).attr('class', 'unsubscribeButton')
                    $(self).text('Unsubscribe')
                }
            });
        }
        else {
                var url = '/Subscribe'
            var self = this
            var data = {
                'userId': userId,
            }
            $.ajax({
                url: url,
                data: data,
                method: 'DELETE',
                success: function() {
                    $(self).attr('class', 'subscribeButton')
                    $(self).text('Subscribe')
                }
            });
        }

    });
//    $('DIV.subUnsubButtons BUTTON').on('click', function(){
//        var userId = $(this).data('userid')
//
//    });
});