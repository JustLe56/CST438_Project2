function refresh(){
    $("#live").load("/hlist/ #refreshed" );
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
}

