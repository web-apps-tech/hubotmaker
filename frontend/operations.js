var ApiEndPoint = "http://133.242.53.17";

function strtHubot(APIKey,hubotId){
  $.ajax({
  type: "POST",
  url: ApiEndPoint "/hubot/"+ hubotId + "/start",
  data: {
    apikey: APIKey
  },
  dataType: "json",
  success: function(data){
    if(data.status){
      alert("started");
    }
  }
  });
}

$(".start").on("click",function(e){
  console.log(e.target.id);
})
