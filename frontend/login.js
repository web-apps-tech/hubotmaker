var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    if(SESSID !== undefined){
	    location.href = "/haas/";
    }
});
$(".LoginButton").on("click",function(){
    $.ajax({
        type: "POST",
	    url: ApiEndPoint + "/user/apikey",
	    cache: false,
	    dataType: "json",
        data: {
	        username: $("#Username").val(),
	        password: $("#Password").val()

	    },
	    success: function(data){
	        if(data.status){
	            $.cookie("SESSID",data.apikey,{expires: 1, path: "/"});
		        location.href = "/haas/";
	        }else{
	            LoginError();
	        }
	    }
    });

});

function LoginError(){
  $(".err-msg").removeClass("hidden");
  usernameForm.parent("div").addClass("has-error");
  passwordForm.parent("div").addClass("has-error");
}



$("#Username, #Password").on("keyup", function(e) {
	if(e.keyCode === 13) {
		$(".LoginButton").trigger("click");
	}
});
