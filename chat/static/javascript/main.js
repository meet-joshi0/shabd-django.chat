
function url_path_userroom(name1, name2) {
  path = "";
  url = "";

  if (name1 > name2) {
    path = name2 + "/" + name1;
    url =
      "http://" +
      window.location.host +
      "/userroom/" +
      name2 +
      "/" +
      name1;
  } else {
    path = name1 + "/" + name2;
    url =
      "http://" +
      window.location.host +
      "/userroom/" +
      name1 +
      "/" +
      name2;

  }
  return url;
}

function short_name_path(name1, name2) {
  names = "";

  if (name1 > name2) {
    names = name2 + "/" + name1;
  } else {
    names = name1 + "/" + name2;

  }
  return names;
}

function friend_unfriend_button(data) {

  if (data == "True") {
    return $("#add").text("Unfriend");
  } else {
    return $("#add").text("Friend");
  }
}

function current_date_time() {
  
  var d = new Date();

  var weekday = [
  "Sun","Mon","Tue", "Wed", "Thu", "Fri", "Sat"]

  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];


  var month = months[ d.getMonth()];
  var hour = d.getHours() > 12 ? d.getHours() - 12 : d.getHours();
  var minute = String(d.getMinutes()).padStart(2, '0');
  var day = weekday[d.getUTCDay()];
    
   var date_time = day+" "+month+" "+hour+":"+minute;
  return   date_time
}


function getProtocol(){
  http_protocol =  window.location.protocol
  return http_protocol
}

function getWebSocketProtocol(){
  let website_protocol = getProtocol()
  let websocket_protocol = "wss://" 
  
  if (website_protocol == "http:"){
    websocket_protocol = "ws://"
  }
  return websocket_protocol;
}


  /* Global Variables */
  let  webSocketProtocol = getWebSocketProtocol() 