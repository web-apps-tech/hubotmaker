var ApiEndPoint = "http://133.242.53.17/";

function generateTbody(hubotId){
var listHTML = "\n\
<tr>\n\ 
<td>" + hubotId + "</td>\n\
<td>OFF</td>\n\
<td>\n\
<button class=\"btn btn-default edit\">Edit</button>\n\
<button class=\"btn btn-info\">Start</button>\n\
<button class=\"btn btn-warning hidden\">Stop</button>\n\
</td>\n\
</tr>\n\
";
    return(listHTML);
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
                        $(".hubot-list-tbody").append(generateTbody(hubotIds[i]);
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
