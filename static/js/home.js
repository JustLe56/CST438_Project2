async function getList(){
    $('#link').html("");
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
}

function getLink(){
    if($('#link').is(':empty')){
        link();
    }else{
        $('#link').html("");
    }
    async function link() {
        let options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };
        let response = await fetch("/api/wishlist-link/", options);
        const json = await response.json();
        console.log(json['personal wishlist hyperlink'])
        $('#link').html("<br><div style='font-size: small; width: 20%' class=\"alert alert-secondary\" role=\"alert\">\n" +
            json['personal wishlist hyperlink'] +
            "</div>")
    }

}