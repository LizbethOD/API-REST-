function getCliente(){

    var request = new XMLHttpRequest();

    usernombre = prompt('Usernombre:')
    password = prompt('Password:')

    var id_Cliente = window.location.search.substring(1);

    console.log("id_Cliente: " + id_Cliente);
    request.open('GET', "https://8000-lizbethod-apirest-h5fixnrf1oq.ws-us54.gitpod.io/clientes/"+ id_Cliente,true);
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

            nombre.value = "Cliente no encontrado";
            email.value = "Cliente no encontrado";
            alert(json.detail);
        }
    };
    request.send();
};