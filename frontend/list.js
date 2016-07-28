var ApiEndPoint = "http://133.242.53.17";

function generateTbody(hubotId){
var listHTML = "\n";
listHTML += "<tr>\n" ;
listHTML += "<td>" + hubotId + "</td>\n";
listHTML += "<td>OFF</td>\n";
listHTML += "<td>\n";
listHTML += "<button class=\"btn btn-default edit\">Edit</button>\n";
listHTML += "<button class=\"btn btn-info\">Start</button>\n";
listHTML += "<button class=\"btn btn-warning hidden\">Stop</button>\n";
listHTML += "</td>\n";
listHTML += "</tr>\n";
    return(listHTML);
}

function getStatus(APIKey,hubotId){
    var status = "OPPAI";
    	$.ajax({
        type: "GET",
	url: ApiEndPoint + "/hubot/" + hubotId + "/status",
	data:{
	    apikey: APIKey
	    },
	dataType: "json",
	success: function(data){
	    if(data.status){
	        status = data.message;
	    }
	}
    });
return status;
}



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
                        $(".hubot-list-tbody").append(generateTbody(hubotIds[i]));
                        console.log(getStatus(SESSID,hubotIds[i]));
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
