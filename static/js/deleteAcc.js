function deleteAccount(){
    $("#delete").submit(async function (event) {
        event.preventDefault();
        let $form = $(this),
            url = $form.attr("action"),
            csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify()
        };

        let response = await fetch(url, options);
        const json = await response.json()
        $("#success").submit();
    });
}