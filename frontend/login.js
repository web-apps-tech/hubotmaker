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
	DataType: "json",
        data: {
	    username: $("#Username").val(),
	    password: $("#Password").val()
	
	},
	success: function(data){
	    if(data.status){
	        $.cookie("SESSID",data.apikey);
		document.href = "../list/";
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
