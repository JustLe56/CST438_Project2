function editList (type){
    if(type === "add") {
        $("#live").html("")
        $('#addItem').one('submit',async function (event) {
            event.preventDefault();
            let $form = $(this),
                i_name = $form.find("input[name = 'name']").val(),
                i_link = $form.find("input[name = 'link_url']").val(),
                i_img_url = $form.find("input[name = 'image_url']").val(),
                i_description = $form.find("input[name = 'description']").val(),
                i_priority = $form.find("select[name = 'priority']").val(),
                action = $form.attr("action"),
                csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
                item = {
                    link_url: i_link,
                    name: i_name,
                    description: i_description,
                    image_url: i_img_url,
                    priority: i_priority
                };

            let options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                    body: JSON.stringify(item)
            };
            console.log("item: ", item);
            let response = await fetch(action, options);
            const json = await response.json();
            if(json.name === i_name){
                $("#live").html("<div class=\"alert alert-success\" role=\"alert\" style=\"font-size: small\">\n<br>"
                +i_name+ " added successfully!\n" +
                    "                </div>")
            }
        });


    }
    // else {
    //
    //     $('#rmItem'+type).one('submit',async function (event) {
    //         $('button[name="rmBtn"]').prop("disabled",true);
    //         event.preventDefault();
    //         let $form = $(this),
    //             url = $form.attr("action"),
    //             csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
    //             creds = {rm: type};
    //
    //         let options = {
    //             method: 'DELETE',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'X-CSRFToken': csrftoken
    //             },
    //             body: JSON.stringify(creds)
    //         };
    //         console.log(creds);
    //         let response = await fetch(url, options);
    //         const json = await response.json();
    //         console.log(json);
    //     });
    // }

}