var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
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
	    alert(data.status);
	    if(data.status){
	        $.cookie("SESSID",data.apikey,{expires: 1, domain: "/"});
		alert("Cookie Set:" + data.apikey);
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
