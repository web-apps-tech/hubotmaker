var ApiEndPoint = "http://133.242.53.17/";
$(document).ready(function(){ 
    var SESSID = $.cookie("SESSID");
    $.ajax({
        type: "GET",
	url: ApiEndPoint + "/user/hubot/list",
	data:{
	    apikey: SESSID
	},
	dataType: "json",
	success: function(data){
	      console.log(data.status);
	}
    });
});
