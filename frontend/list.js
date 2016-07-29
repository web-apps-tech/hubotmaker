$(".create-new").on("click", function() {
    $('#CreateModal').modal("show");
});
$(".delete").on("click", function() {
    $('#DeleteConfirm').modal("show");
});
$("#create-submit").on("click",function(){
  var APIKey = $.cookie("SESSID");
  var envs = [];
  var slackToken = $("#SlackToken").val();
  var tags = $("#create-functions .checkbox label");
  for(var i=0; i < tags.length; i++){
    var checkboxId = "#" + tags[i].children[0].id;
      if($(checkboxId).prop("checked")){
        console.log(tags[i].id.split("_")[1]);
        envs.push(tags[i].id.split("_")[1]);
      }
  }
createHubot(APIKey,slackToken,envs);
});

var ApiEndPoint = "http://133.242.53.17";


function getHubotEnvs(APIKey, hubotId) {
    var envs;
    $.ajax({
        type: "GET",
        url: ApiEndPoint + "/hubot/" + hubotId + "/env",
        data: {
            apikey: APIKey,
        },
        dataType: "json",
        async: false,
        success: function(data) {
            if (data.status) {
                envs = data.message;
            }
        }

    });
    return envs;
}


function generateTbody(hubotId) {
    var listHTML = "\n";
    listHTML += "<tr>\n";
    listHTML += "<td>" + hubotId + "</td>\n";
    listHTML += "<td id='st_" + hubotId + "'>OFF</td>\n";
    listHTML += "<td>\n";
    listHTML += "<button class=\"btn btn-default edit\">Edit</button>\n";
    listHTML += "<button class=\"btn btn-info start \" hidden id='start_" + hubotId + "'>Start</button>\n";
    listHTML += "<button class=\"btn btn-warning stop hidden\" id='stop_" + hubotId + "'>Stop</button>\n";
    listHTML += "</td>\n";
    listHTML += "</tr>\n";
    return (listHTML);
}

function generateCheckboxes(prefix, scriptName) {
    var divHTML = "\n"

    divHTML += "<div class=\"checkbox\">\n";
    divHTML += "<label id=\"" + prefix + "_" + scriptName + "\">";
    divHTML += "<input type=\"checkbox\" id=\"" + prefix + "_" + scriptName + "_cb" + "\">\n";
    divHTML += scriptName + "</label>";
    divHTML += "</div>\n";

    return (divHTML);
}

function getStatus(APIKey, hubotId) {
    var status = "OPPAI";
    $.ajax({
        type: "GET",
        url: ApiEndPoint + "/hubot/" + hubotId + "/status",
        data: {
            apikey: APIKey
        },
        dataType: "json",
        success: function(data) {
            if (data.status) {
                var status = data.message;
                var st_id = "#st_" + hubotId;
                var start_id = "#start_" + hubotId;
                var stop_id = "#stop_" + hubotId;
                if (status) {
                    $(st_id).text("ON");
                    $(start_id).addClass("hidden");
                    $(stop_id).removeClass("hidden");
                } else {
                    $(st_id).text("OFF");
                    $(start_id).removeClass("hidden");
                    $(stop_id).addClass("hidden");
                }
            }
        }
    });
}

function setAvailableScripts() {
    $.ajax({
        type: "GET",
        url: ApiEndPoint + "/available_scripts",
        dataType: "json",
        success: function(data) {
            if (data.status) {
                for (var i = 0; i < data.message.length; i++) {
                    $("#create-functions").append(generateCheckboxes("create", data.message[i]));
                    $("#edit-functions").append(generateCheckboxes("edit", data.message[i]));
                }
            }
        }
    });

}

function createHubot(APIKey,slackToken,scriptEnvs){
  $.ajax({
  type: "POST",
  url: ApiEndPoint + "/hubot",
  data: {
    apikey: APIKey,
    slack_token: slackToken,
    script_env: JSON.stringify(scriptEnvs)
  },
  dataType: "json",
  success: function(data){
    if(data.status){
      alert("created");
    }
  }
  });
}


$(document).ready(function() {
    var SESSID = $.cookie("SESSID");
    if (SESSID !== undefined) {
        $.ajax({
            type: "GET",
            url: ApiEndPoint + "/user/hubot/list",
            data: {
                apikey: SESSID
            },
            dataType: "json",
            success: function(data) {
                var hubotIds = data.message;
                for (var i = 0; i < hubotIds.length; i++) {
                    $(".hubot-list-tbody").append(generateTbody(hubotIds[i]));
                    getStatus(SESSID, hubotIds[i]);
                    $(".start").on("click", function(e) {
                        startHubot(SESSID, e.target.id.split("_")[1]);
                    });
                    $(".stop").on("click", function(e) {
                        stopHubot(SESSID, e.target.id.split("_")[1]);
                    });
                }
                $(".edit").on("click", function(e) {
                    var hubotId = e.target.parentNode.parentNode.children[0].textContent;
                    var hubotEnvs = getHubotEnvs(SESSID, hubotId);
                    var slackToken = hubotEnvs["HUBOT_SLACK_TOKEN"];
                    $('#EditModal').modal("show");
                    $("#EditSlackToken").val(slackToken);
                    var checkboxes = $("#edit-functions .checkbox label");
                    for (var i = 0; i < checkboxes.length; i++) {
                        var scriptName = checkboxes[i].id.split('_')[1];
                        console.log("scriptName:" + scriptName);
                        var checkboxbId = "#" + "edit_" + scriptName + "_cb";
                        if (hubotEnvs[scriptName]) {
                            $(checkboxbId).prop("checked", true);
                        } else {
                            $(checkboxbId).prop("checked", false);
                        }

                    }

                });
                setAvailableScripts();
            }
        });
    } else {
        location.href = "../login/";
    }
});

$(".logout").on("click", function() {
    $.cookie("SESSID", '', {
        expires: -1,
        path: "/"
    });
    location.href = "../login/";
});
