function deleteCliente(){

    var request = new XMLHttpRequest();

    usernombre = prompt('Usernombre:')
    password = prompt('Password:')

    var id_cliente = window.location.search.substring(1);

    console.log("id_cliente: " + id_cliente);
    request.open('DELETE', "https://8000-lizbethod-apirest-h5fixnrf1oq.ws-us54.gitpod.io/clientes/?id_cliente="+ id_cliente,true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(usernombre + ":" + password))
    request.setRequestHeader("content-Type", "application/json");

    request.onload = () => {
        
        const response = request.responseText;
        const json = JSON.parse(response);     
        const status = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }
        else if (request.status == 202){
            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            alert(json.message);
            window.location.replace("post_cliente.html")
        }
    };
    request.send();
}