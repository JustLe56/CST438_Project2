function editList(i){
    $("#edited").submit(async function (event){
            event.preventDefault();
            $('#removeBtn').prop("disabled",true);
            $('#updateButton').prop("disabled",true);
            event.stopImmediatePropagation();
            let $form = $(this),
                url = $form.attr("action"),
                i_name = $form.find("input[name = 'name']").val(),
                i_link = $form.find("input[name = 'link_url']").val(),
                i_img_url = $form.find("input[name = 'image_url']").val(),
                i_description = $form.find("input[name = 'description']").val(),
                i_priority = $form.find("select[name = 'priority']").val(),
                csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
                item = {
                    index: i,
                    link_url: i_link,
                    name: i_name,
                    description: i_description,
                    image_url: i_img_url,
                    priority: i_priority
                };

            let options = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                    body: JSON.stringify(item)
            };
            console.log("item: ", item);
            let response = await fetch(url, options);
            const json = await response.json();
            console.log(json)
            if(json.name === i_name){
                $('#msg').html("<br><div style='font-size: small' class='alert alert-secondary' role='alert'>" +
                   "loading..." +
                   "</div>");
                await getList();
                $('#msg').html("");
                location.reload();
            }
        });
}

async function prefill(i){
    let options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };
    console.log("here")
        let response = await fetch("/api/item/"+i, options);
        const json = await response.json();
        console.log(json);
    $("#itemNameInput").val(json.name);
    $("#itemDesc").val(json.description);
    $("#urlInput").val(json.link_url);
    $("#urlImageInput").val(json.image_url);
    $("#priority").val(json.priority);
}

function remove(){
    $("#edited").submit(async function (event){
        $('#updateButton').prop("disabled",true);
        $('#removeBtn').prop("disabled",true);
        event.preventDefault();
        let $form = $(this),
            url = $form.attr("action"),
            csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        };

        let response = await fetch(url, options);
        const json = await response;
        if(json.status===204){
            $('#msg').html("<br><div style='font-size: small' class='alert alert-secondary' role='alert'>" +
                   "loading..." +
                   "</div>");
            await getList()
            window.location.href = "/";
        }

    });
}
async function getList(){
    let options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };
    let response =  await fetch("/api/listitems/", options);
    let json = await response;
    console.log(json)
    if( json.status ===200){
        json = await response.json()
    }

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