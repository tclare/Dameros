$(document).ready(function() {
  $("textarea").change(inputChanged);
});

function inputChanged(){
  console.log("Here");
  // var v = document.getElementById("first-landing-paragraph").value; <== normal JS
  // var v = $('#first-landing-paragraph') // <== jquery
  //console.log($(this));
  var admin_id = $(this).attr('id');
  var admin_val = $(this).val();
  var o = {};
  o[admin_id] = admin_val;
  console.log(o);
/*
  // Make a request to the server.
  var xhttp = new XMLHttpRequest();
  // Step 1: send request to server.
  xhttp.open("PUT", "http://dameros.herokuapp.com/put_content/", true); // GET, POST (add something new), PUT (modify something), DELETE (get rid of something),
  xhttp.send(JSON.stringify(o));
  xhttp.onreadystatechange = function (e) {
    if (xhttp.readyState == 4) {
      var response = xhttp.responseText;
      var parsed_response = JSON.parse(response);
      if (parsed_response["success"] == "yes") console.log("operation successful!");
      else console.log("error! " + parsed_response["error"]);
      // Response will either be one of these two:
      // {"success": "yes"}
      // {"success": "no", "error": "error message asdf asdf asdf"}
    }
  }*/


  /* JSON example: {
    "key": "value",
    "key2": [
      {"key": "value"}
    ]
  }*/

}
