$(document).ready(function(){
    $('#admin-modal').modal({backdrop: 'static', keyboard: false});
    $('#admin-modal').modal('show');
    $('#login').click(send_password);
});

function send_password() {
    var pw = $('#pw').val();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", protocol_hostname_port() + "/login", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"password": pw}));
    xhr.onreadystatechange = function (e) {
        if (xhr.readyState == 4) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);
            if (response["success"] == "yes") window.location.href = protocol_hostname_port() + "/admin";
        }
    }
}