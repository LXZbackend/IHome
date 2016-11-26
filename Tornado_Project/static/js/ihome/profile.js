function showSuccessMsg() {
    $('.save_success').fadeIn('fast', function() {
        setTimeout(function(){
            $('.save_success').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    //上传头像
    $("#form-avatar").submit(function(e){
        e.preventDefault();
        console.log("上传头像")
        $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }
            }
        };
        $(this).ajaxSubmit(options);
    });




 $("#form-name").submit(function(e){
        e.preventDefault();
        // userName = $('.image_uploading').fadeIn('fast');
        userName=$("#user-name").val()
        console.log(userName) 
        // console.log(data)
        var options = {
            url:"/api/profile/name",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    // $('.image_uploading').fadeOut('fast');
                    console.log(data.up_avatar)
                    console.log(data.name)
                }
            }
        };
        $(this).ajaxSubmit(options);
    });


$.get("/api/check_login", function(data) {
        if ("0" == data.errno) {
            console.log(data)
            console.log('********8')
            console.log(data.data.up_avatar)
             $("#user-avatar").attr('src',data.data.up_avatar)
            console.log(data.data.name)
             $("#user-name").val(data.data.name)
             console.log('********8')

        } else {
              location.href = "/login.html";
        }
    }, "json");










})