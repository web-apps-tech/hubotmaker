var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    alert(SESSID);
    if(SESSID !== undefined){    
	document.href = "../list/";
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
    //ろぐいんえら
}
