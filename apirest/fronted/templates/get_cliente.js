function get_Cliente(){

    var request = new XMLHttpRequest();
    var token = sessionStorage.getItem('item');
    console.log(token)
    
    var id_cliente = window.location.search.substring(1);

    console.log("id_cliente: " + id_cliente);
    
    request.open('GET', "https://8000-lizbethod-apirest-n3l0fmlt2en.ws-us60.gitpod.io/clientes/"+ id_cliente,true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + token)
    request.setRequestHeader("content-type", "application/json");

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

            console.log("Nombre: "+ json[0].nombre);
            console.log("Email: "+ json[0].email);

            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");

            nombre.value = json[0].nombre;
            email.value = json[0].email;
        }
        else if(status==404){
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");

            nombre.value = "None";
            email.value = "None";
            alert("Cliente no encontrado");
        }
    }
    request.send();
}