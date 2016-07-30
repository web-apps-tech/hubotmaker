var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    if(SESSID !== undefined){
	    location.href = "../";
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
		        location.href = "../list/";
	        }else{
	            LoginError();
	        }
	    }
    });

});

function LoginError(){
    console.log("error");
    //�낮���񂦂�
}



$("#Username, #Password").on("keyup", function(e) {
	if(e.keyCode === 13) {
		$(".LoginButton").trigger("click");
	}
});
