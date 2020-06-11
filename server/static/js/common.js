// FUNCTION (utility): protocol_hostname_port
// params: none
// returns string: protocol, hostname, port from current URL. Avoids hardcoding in API calls.
function protocol_hostname_port() {
    return location.protocol + '//' + location.hostname + (location.port ? ':'+location.port: '');
  }