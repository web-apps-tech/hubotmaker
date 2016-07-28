$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    if(SESSID !== undefined){
	document.href = "../list/";
    }
});
