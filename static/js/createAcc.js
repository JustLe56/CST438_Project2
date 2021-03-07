function matchPass(){
    let password = $('input[name = "password"]');
    let confirmPass = $("#confirmPass");
    let valMsg = $("#valMsg");

    if(password.val() === confirmPass.val()){
        valMsg.html("");
        return true;
    }else{
        valMsg.html("<br><div class='alert alert-warning' role='alert'> passwords don't match </div>");
        valMsg.css("font-size", "small");
        return false;
    }
}