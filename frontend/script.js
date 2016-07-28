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

    $.ajax({
        type: "POST",
        url: ApiEndPoint + "user",
        cache: false,
        data: {
            username: $("#Username").val(),
            password: $("#Password").val()
        },
	dataType: "json",
        success: function(data) {
		console.log(data);
    		if (data.status == true) {
                UserActivate();
            } else {
		$(".err-msg").removeClass("hidden");
                $("#Username").parent("div").addClass("has-error");
                $("#Password").parent("div").addClass("has-error");
            }
	}
    });
}

function UserActivate() {

    $.ajax({
        type: "PUT",
        url: ApiEndPoint + "user/activate",
        cache: false,
        data: {
            username: $("#Username").val(),
            password: $("#Password").val()
        },
	dataType: "json",
        success: function(data) {
            if (data.status == true) {
                GenerateAPIKey();
            }
	 }
    });
}

function GenerateAPIKey() {

    $.ajax({
        type: "POST",
        url: ApiEndPoint + "user/apikey",
        cache: false,
        data: {
            username: $("#Username").val(),
            password: $("#Password").val()
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


}



//$(".UserRegistSubmit").on("click",UserRegistSubmit());
