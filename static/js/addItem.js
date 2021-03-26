function editList (type){
     $("#live").html("")
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
                 $('#live').html("<br><div style='font-size: small' class='alert alert-secondary' role='alert'>" +
                   "loading.." +
                   "</div>");
                await getList();
                $("#live").html("<br><div style='font-size: small' class='alert alert-success' role='alert'>" +
                   i_name+" Added successfully" +
                   "</div>");
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
async function getList(){
    let options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };
    let response =  await fetch("/api/listitems/", options);
    const json =  await response.json();
    console.log(json)
    let newReq = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    };
    let resp = await fetch("/load_items/", newReq)
    let jsn = await resp
    console.log(jsn)
}
