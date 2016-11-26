function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
	console.log('********8')
	 $.get("/api/check_login", function(data) {
        if ("0" == data.errno) {

        	console.log('********8')
				    $(".menu-text #user-name").html(data.data.name)
				    console.log(data.data.mobile)
             $(".menu-text #user-mobile").html(data.data.mobile)
             console.log('********8')
             $("#user-avatar").attr("src",data.data.up_avatar)

        } else {
              location.href = "/login.html";
        }
    }, "json");










})