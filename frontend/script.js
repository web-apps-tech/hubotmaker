var ApiEndPoint = "http://133.242.53.17/";

$(".create-new").on("click", function() {
    $('#CreateModal').modal("show")
});
$(".edit").on("click", function() {
    $('#EditModal').modal("show")
});
$(".delete").on("click", function() {
    $('#DeleteConfirm').modal("show")
});
$(".UserRegistSubmit").on("click", UserRegistSubmit);




function UserRegistSubmit() {
    var username = $("#Username").val()
    var password = $("#Password").val()
    $.ajax({
        type: "POST",
        url: ApiEndPoint + "user",
        cache: false,
        data: {
            username: username,
            password: password
        },
	dataType: "json",
        success: function(data) {
		console.log(data);
    		if (data.status == true) {
                UserActivate(username, password);
            } else {
		$(".err-msg").removeClass("hidden");
                $("#Username").parent("div").addClass("has-error");
                $("#Password").parent("div").addClass("has-error");
            }
	}
    });
}

function UserActivate(username, password) {

    $.ajax({
        type: "PUT",
        url: ApiEndPoint + "user/activate",
        cache: false,
        data: {
            username: username,
            password: password
        },
	dataType: "json",
        success: function(data) {
            if (data.status == true) {
                GenerateAPIKey(username, password);
            }
	 }
    });
}

function GenerateAPIKey(username, password) {

    $.ajax({
        type: "POST",
        url: ApiEndPoint + "user/apikey",
        cache: false,
        data: {
            username: username,
            password: password
        },
	dataType: "json",
        success: function(data) {
            if (data.status == true) {
                showAPIKey(data.apikey);
            }
	 }
    });

}

function showAPIKey(APIKey){

    $(".RegisterCompleted").removeClass("hidden");
    $(".login-form").addClass("hidden");
    $(".api-key").text(APIKey);
    $(".api-key").val(APIKey);

}



//$(".UserRegistSubmit").on("click",UserRegistSubmit());
