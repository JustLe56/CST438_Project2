function editList (type){
    if(type === "add") {

        $('#addItem').one('submit',async function (event) {
            event.preventDefault();
            let $form = $(this),
                item = $form.find("input[name = 'rm']").val(),
                i_name = $form.find("input[name = 'name']").val(),
                i_url = $form.find("input[name = 'url']").val(),
                i_img_url = $form.find("input[name = 'img_url']").val(),
                i_description = $form.find("input[name = 'description']").val(),
                i_priority = $form.find("select[name = 'priority']").val(),
                action = $form.attr("action"),
                csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
                creds = {
                    rm: item,
                    name: i_name,
                    url: i_url,
                    img_url: i_img_url,
                    description: i_description,
                    priority: i_priority
                };

            let options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(creds)
            };
            console.log(creds);
            let response = await fetch(action, options);
            const json = await response.json()
            console.log(json);
            refresh()
        });


    } else {

        $('#rmItem'+type).one('submit',async function (event) {
            $('button[name="rmBtn"]').prop("disabled",true);
            event.preventDefault();
            let $form = $(this),
                url = $form.attr("action"),
                csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
                creds = {rm: type};

            let options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(creds)
            };
            console.log(creds);
            let response = await fetch(url, options);
            const json = await response.json();
            console.log(json);
            refresh()
        });
    }
}

function refresh(){
    $("#live").load("/list/ #refreshed" );

}