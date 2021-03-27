function resetVal(){
    $("#valMsg").html("")
}

function createAccount(){

        $("#credentials").submit(async function (event) {
            if(matchPass()===true) {
                event.preventDefault();
                let $form = $(this),
                    usr = $form.find("input[name = 'username']").val(),
                    pass = $form.find("input[name='password']").val(),
                    url = $form.attr("action"),
                    csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
                    creds = {username: usr, password: pass};

                let options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(creds)
                };

                let response = await fetch(url, options);

                if(response.status === 201){
                    $("#success").submit();
                }else{
                    let json = await response.json();
                    $("#valMsg").html(
                        "<br><div style='font-size: small' class='alert alert-secondary' role='alert'>"+ json.username
                        +"</div>"
                    );
                }
            }
        });

}

function matchPass(){
    let password = $('input[name = "password"]');
    let confirmPass = $("#confirmPass");
    let valMsg = $("#valMsg");

    if(password.val() === confirmPass.val()){
        valMsg.html("");
        return true;
    }else{
        valMsg.html("<br><div style='font-size: small' class='alert alert-secondary' role='alert'> passwords don't match </div>");
        valMsg.css("font-size", "small");
        return false;
    }
}