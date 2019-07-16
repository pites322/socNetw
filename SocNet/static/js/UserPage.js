$(document).ready(function(){
//    add csrf_token to ajax
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
//
    $('.AvatarChange').click(function(){
        if ($('.AvatarChangeButtons').css('display')=='none' && $('.AvatarChangeList').css('display')=='none'){
            $('.AvatarChangeButtons').css('display', 'flex');
            $('.AvatarChangeList').css('display', 'flex');}
        else{
            $('.AvatarChangeButtons').css('display', 'none');
            $('.AvatarChangeList').css('display', 'none');
        }
    });
//    mark chosen avatar picture and add it to avatar place after click on avatar picture
    var avatar = '';
    var AvatarManualId = '';
    $('.avatarListPicture').click(function(){
        if (AvatarManualId != ''){
            $('#avatarListElem' + AvatarManualId).css('background-color', 'red')};
        if (avatar == ''){
            avatar = $('.avatar').attr('src')};
        AvatarManualId = $(this).data('id');
        var src = $(this).data('src');
        $('#avatarListElem' + AvatarManualId).css('background-color', 'blue');
        $('.avatar').attr('src', src);
    })
//    add manual avatar picture after click on 'chanel' button
    $('.avatarCancel').click(function(){
        if (avatar != ''){
        $('.avatar').attr('src', avatar);
        }
    });
//    open dell menu after hover on avatar picture
    var idDellMenu = ''
    $('.avatarListPicture, .dellMenu, .avatarMenuList').mouseover(function(){
        var elemId = $(this).data('id');
        if ($('#dellMenu' + elemId).css('display') == 'none'){
        $('#dellMenu' + idDellMenu).slideToggle();
        idDellMenu = elemId;
        $('#dellMenu' + elemId).slideToggle();}
    });
//    delete chosen avatar picture from avatar picture list after click on 'delete' button
    $('.dellMenu').click(function(){
        var id = $(this).data('idavatrtodell');
        var url = '/AvatarSupActions'
        var data = {
            'idToDelete': id,
        }
        $.ajax({
            url: url,
            data: data,
            method: 'DELETE',
            success: function(){
                $('#elemAnatarList'+ id).remove()
            },
        });
    });
//    save chosen avatar
    $('.avatarSave').on('click', function(){
        var url = '/AvatarSupActions'
        if (AvatarManualId != ''){
            var data = {
                'AvatarManualId': AvatarManualId,
            }
            $.ajax({
                url: url,
                data: data,
                method: 'PUT',
            });
            location.reload();
        }
    });
//    first 10 posts and display next 10 after scroll
    var postListLength = 10
    $('DIV.postList DIV:nth-child(-n +' + postListLength +')').css('display', 'block');
    jQuery(window).scroll(function() {
    if(jQuery(window).scrollTop()+jQuery(window).height()>=jQuery(document).height()){
			postListLength += 10;
			$('DIV.postList DIV:nth-child(-n +' + postListLength +')').css('display', 'block');
		};
	});
})