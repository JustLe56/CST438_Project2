function resetVal(){
    $("#valMsg").html("")
}

function login(){
    $("#credentials").submit(function (event){
        event.preventDefault();
        let $form = $(this),
            usr = $form.find("input[name = 'username']").val(),
            pass = $form.find("input[name='password']").val(),
            url = $form.attr("action"),
            creds = { username: usr, password: pass },
            posting = $.post(url, JSON.stringify(creds));

        posting.fail(function (xhr, status, error){
            $("#valMsg").html("<br><div style='font-size: small' class='alert alert-secondary' role='alert'>" +
                   "Wrong username/password" +
                   "</div>");
            console.log(error)
        })

        posting.done(function (data){
           let content = $(data).find("#content");
           $("#valMsg").empty().append(content);
           console.log(content);
           console.log(content.status)
           if(content.prevObject[0].detail === "Success"){
               window.location.href = "/";
           }
        });
    });
}