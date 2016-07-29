var ApiEndPoint = "http://133.242.53.17";

function startHubot(APIKey, hubotId) {
    $.ajax({
        type: "POST",
        url: ApiEndPoint + "/hubot/" + hubotId + "/start",
        data: {
            apikey: APIKey
        },
        dataType: "json",
        success: function(data) {
            if (data.status) {
                getStatus(APIKey, hubotId);
            }
        }
    });
}

function stopHubot(APIKey, hubotId) {
    $.ajax({
        type: "POST",
        url: ApiEndPoint + "/hubot/" + hubotId + "/stop",
        data: {
            apikey: APIKey
        },
        dataType: "json",
        success: function(data) {
            if (data.status) {
                getStatus(APIKey, hubotId);
            }
        }
    });
}
