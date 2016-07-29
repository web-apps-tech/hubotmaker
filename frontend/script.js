var ApiEndPoint = "http://133.242.53.17/";

$(".UserRegistSubmit").on("click", UserRegistSubmit);

$(".user-delete").on("click",function(){
  $("#UserDeleteConfirm").modal("show");
});


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
            if (data.status) {
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
            if (data.status) {
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
            if (data.status) {
                showAPIKey(data.apikey);
            }
        }
    });

}

function showAPIKey(APIKey) {

    $(".RegisterCompleted").removeClass("hidden");
    $(".login-form").addClass("hidden");
    $.cookie("SESSID", APIKey, {
        expires: 1,
        path: "/"
    });

}
