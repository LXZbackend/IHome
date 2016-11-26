// function showSuccessMsg() {
//     $('.popup_con').fadeIn('fast', function() {
//         setTimeout(function(){
//             $('.popup_con').fadeOut('fast',function(){}); 
//         },1000) 
//     });
// }

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}




$(document).ready(function(){

$.get("/api/check_login", function(data) {
        if ("0" == data.errno) {
        	name = data.data.real_name
        	id = data.data.id_card
        	console.log(name)
        	console.log(id)

        	if(name&&id!=null){
            console.log(data.data.real_name)
             $("#real-name").val(data.data.real_name).attr("disabled","disabled")
           
            console.log(data.data.id_card)
             $("#id-card").val(data.data.id_card).attr("disabled","disabled")

          	$(".btn-success").hide()

          
          	}

        } else {
              location.href = "/login.html";
        }
    }, "json");


})



    $("#form-auth").submit(function(e){
        e.preventDefault();
        real_name=$("#real-name").val()
				id_card = $("#id-card").val()

				console.log(real_name)
				console.log(id_card)

				data = {
					real_name:real_name,
					id_card:id_card
				}

				$.ajax({
						url:"/api/profile/auth",
						type:"post",
						data:JSON.stringify(data),
						contentType: "application/json",
						dataType:"json",
						headers:{
							"X-XSRFTOKEN":getCookie("_xsrf"),
						},
						success:function(data){

							if('0'==data.errno){
								console.log('更新成功')

							}

						}



    });

	location.href = "/auth.html";

console.log("阿达速冻")
 
})

