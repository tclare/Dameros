// FUNCTION (utility): protocol_hostname_port
// params: none
// returns string: protocol, hostname, port from current URL. Avoids hardcoding in API calls.
function protocol_hostname_port() {
    return location.protocol + '//' + location.hostname + (location.port ? ':'+location.port: '');
}

// FUNCTION : newApplication. Submits apply form data.
// params: none. Called after 'Submit' button is clicked
// returns: none.
function newApplication(){
    var name = $('#apply-name').val();
    var email = $('#apply-email').val();
    var sport = $('#apply-sport').val();
    var donationAmount = $('#apply-donation-amount').val();
    var philanthropicInterest = $('#apply-philanthropic-interests').val();
    var o = {'name': name, 'email': email, 'sport': sport, 'donationAmount': donationAmount, 'philanthropicInterest': philanthropicInterest};
    var xhttp = new XMLHttpRequest(); // step 1
    xhttp.open("POST", protocol_hostname_port() + "/apply_response", true); // step 2
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); // step 2.5
    xhttp.send(JSON.stringify(o)); // step 3
    xhttp.onreadystatechange = function (e) {
      if (xhttp.readyState == 4) {
        var response = xhttp.responseText;
        console.log(response);
      }
    }
  }