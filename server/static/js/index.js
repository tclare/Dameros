$(document).ready(function() {
  $("textarea").change(textInputChanged); // all text inputs are <textarea>s
  $("textarea").on('input', saveButtonAppear);
  $("input").change(imageInputChanged);  // all image inputs are <input>s

});

// FUNCTION (utility): protocol_hostname_port
// params: none
// returns string: protocol, hostname, port from current URL. Avoids hardcoding in API calls.
function protocol_hostname_port() {
  return location.protocol + '//' + location.hostname + (location.port ? ':'+location.port: '');
}

function saveButtonAppear() { 
  var textarea_div = $(this).parent();
  var label_div = textarea_div.parent();
  if (!(label_div.has("button").length)) textarea_div.before('<button class="btn admin-save-button" onclick="saveButtonDisappear()">Save</button>');
}

function saveButtonDisappear() {
  $(this).remove();
}

function textInputChanged(){
  console.log("Here");
  // var v = document.getElementById("first-landing-paragraph").value; <== normal JS
  // var v = $('#first-landing-paragraph') // <== jquery
  //console.log($(this));
  var admin_id = $(this).attr('id');
  saveButtonAppear($(this).parent());
  var admin_val = $(this).val();
  var o = {id: admin_id, value: admin_val};
  o[admin_id] = admin_val;

  // Make a request to the server.
  var xhttp = new XMLHttpRequest();
  // Step 1: send request to server.
  xhttp.open("PUT", protocol_hostname_port() + "/text_content", true); // GET, POST (add something new), PUT (modify something), DELETE (get rid of something),
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
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
  }


  /* JSON example: {
    "key": "value",
    "key2": [
      {"key": "value"}
    ]
  }*/

}


function imageInputChanged() {
  var admin_id = $(this).attr('id');
  var form_data = new FormData();
  form_data.append(admin_id, $('#' + admin_id)[0].files[0]);
  console.log(form_data);
  
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", protocol_hostname_port() + "/image_content", true);
  xhttp.send(form_data);
  xhttp.onreadystatechange = function (e) {
    if (xhttp.readyState == 4) {
      var response = xhttp.responseText;
      console.log(response);
    }
  }
  
}
