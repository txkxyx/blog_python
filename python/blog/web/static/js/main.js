$(function(){
    const hurger = $('.navbar-burger');
    $(hurger).click(function(){
        const id = $(hurger).data('target');
        if($('#'+id).hasClass('is-active') && $(hurger).hasClass('is-active')){
            $('#'+id).removeClass('is-active');
            $(hurger).removeClass('is-active');
        }else{
            $('#'+id).addClass('is-active');
            $(hurger).addClass('is-active');
        }
        
    })
    $('.confirm').click(function(){
        $('#confirm').addClass('is-active');
        $('#cmail').text($('#mail').val());
        $('#cname').text($('#name').val());
        $('#cpassword').text($('#password').val());
        $('#cconf_password').text($('#conf_password').val());
        $('#cnow_password').text($('#now_password').val());
    });

    $('.close').click(function(){
        $('.modal').removeClass('is-active');
        $('#modal-delete').removeClass('is-active');
    })

    $('.dlg-delete').click(function(){
        $('#modal-delete').addClass('is-active');
    })
})