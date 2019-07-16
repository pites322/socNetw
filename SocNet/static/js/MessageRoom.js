$(document).ready(function(){
//   add csrf_token to ajax
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
//    take id of interlocutor
    var interlocutor = $('DIV.messageList').data('interlocutorid')
//    open support menu after hover mouse on message and close it on previous message
    var idDellMenu = ''
    $(document).on ("mouseenter",'DIV.messageList DIV', function(){
        var elemId = $(this).data('id');
        if ($('#changeMenuElem' + elemId).css('display') == 'none'){
        $('#changeMenuElem' + idDellMenu).slideToggle();
        idDellMenu = elemId;
        $('#changeMenuElem' + elemId).slideToggle();}
    });
//    delete message after click on 'dell' string in span
    $(document).on("click", 'SPAN.dellMessage', function(){
        var elemId = $(this).data('id');
        var url = '/MessageActions';
        var data = {
            'idToDelete': elemId,
            'interlocutor': interlocutor
        };
        $.ajax({
            url: url,
            data: data,
            method: 'DELETE',
            success: function(){
                $('#Message'+ elemId).remove()
            },
        });
    });
//    add data on textarea after click on 'change' string and change
    var IdMessageToChange = ''
    $(document).on("click", 'SPAN.changeMessage', function(){
        IdMessageToChange = $(this).data('id');
        var messageText = $('DIV#Message' + IdMessageToChange + ' DIV.messageBody').text()
        $('DIV.input TEXTAREA').val(messageText)
    });
//    clean textarea and IdMessageToChange after click on button clear
    $(document).on("click", 'button.cleanTextarea', function(){
        dMessageToChange = ''
        $('DIV.input TEXTAREA').val('')
    });
//    create new message or change created
    $('DIV.input BUTTON.addMessage').on("click", function(){
        var text = $('DIV.input TEXTAREA').val();
        if (text){
            if (IdMessageToChange == ''){
            var method = 'POST'
            var data = {
                'text': text,
                'interlocutor': interlocutor,
            };
            }else{
            var method = 'PUT'
            var data = {
                'messageId': IdMessageToChange,
                'text': text,
            };
            }
            var url = '/MessageActions';
            $.ajax({
                url: url,
                data: data,
                method: method,
                success: function(data){
                    if (IdMessageToChange == '') {
                    $('.messageList DIV.message:last-child').after('<div class="sent message"><div class="changeMenu"><span class="dellMessage">dell</span><span class="changeMessage">change</span></div><div class="messageBody"></div><div class="date"></div></div>');
                    $('.messageList DIV.message:last-child').attr('data-id', data['id']).attr('id', 'Message' + data['id']);
                    $('.messageList DIV.message:last-child .changeMenu').attr('id', 'changeMenuElem' + data['id']);
                    $('.messageList DIV.message:last-child .dellMessage').attr('data-id', data['id']);
                    $('.messageList DIV.message:last-child .changeMessage').attr('data-id', data['id']);
                    $('.messageList DIV.message:last-child .messageBody').text(text);
                    $('.messageList DIV.message:last-child .date').text(data['date']);
                    $('DIV.input TEXTAREA').val('')
                    }else{
                    $('DIV#Message' + IdMessageToChange + ' DIV.messageBody').text(text)
                    IdMessageToChange = ''
                     $('DIV.input TEXTAREA').val('')
                    }
                },
            });
        };
    });

});