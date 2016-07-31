var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    if(SESSID !== undefined){
	    location.href = "/";
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
		        location.href = "/";
	        }else{
	            LoginError();
	        }
	    }
    });

});

function LoginError(){
  $(".err-msg").removeClass("hidden");
  $("#Username").parent("div").addClass("has-error");
  $("#Password").parent("div").addClass("has-error");
}



$("#Username, #Password").on("keyup", function(e) {
	if(e.keyCode === 13) {
		$(".LoginButton").trigger("click");
	}
});
