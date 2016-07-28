var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function(){
    var SESSID = $.cookie("SESSID");
    if(SESSID !== undefined){
        $.ajax({
            type: "GET",
	        url: ApiEndPoint + "/user/hubot/list",
	        data:{
	            apikey: SESSID
	        },
	        dataType: "json",
	        success: function(data){
	            console.log(data.status);
		    var hubotIds = data.message;
		    for (var i=0; i < hubotIds.length; i++){
		        console.log(hubotIds[i]);
		    } 
	        }
        });
    }else{
        location.href = "../login/";
    }
});

$(".logout").on("click",function(){
    $.cookie("SESSID",'',{expires: -1 ,path: "/"});
    location.href = "../login/";
});
