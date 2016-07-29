var ApiEndPoint = "http://133.242.53.17/";

$(".UserRegistSubmit").on("click", UserRegistSubmit);

$(".user-delete").on("click",function(){
  $("#DeleteUserConfirm").modal("show");
});

$(".delete-user-modal-button").on("click",UserDeleteSubmit);


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

function UserDeleteSubmit(){
  var usernameForm = $("#delete-user-username")
  var passwordForm = $("#delete-user-password")
  $.ajax({
      type: "DELETE",
      url: ApiEndPoint + "user",
      cache: false,
      data: {
          username: usernameForm.val(),
          password: passwordForm.val()
      },
      dataType: "json",
      success: function(data) {
          if (data.status) {
              logout();
          } else {
              $(".err-msg").removeClass("hidden");
              usernameForm.parent("div").addClass("has-error");
              passwordForm.parent("div").addClass("has-error");
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
