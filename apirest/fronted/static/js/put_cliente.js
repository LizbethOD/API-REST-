function putCliente(){

    var request = new XMLHttpRequest();

    usernombre = prompt('Usernombre:');
    password = prompt('Password:');

    var id_cliente = window.location.search.substring(1);
    
    let id_clienteactual = id_cliente;
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");
    let payload = {
        "id_cliente": id_clienteactual,
        "nombre": nombre.value,
        "email" : email.value,
    }

    console.log("id_cliente: " + id_cliente);
    console.log("nombre: " + nombre.value);
    console.log("email: "  + email.value);
    console.log(payload);
    
    request.open('PUT', "https://8000-lizbethod-apirest-h5fixnrf1oq.ws-us54.gitpod.io/clientes/",true);
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
            window.location.replace("get_clientes.html")
        }
    };
    request.send(JSON.stringify(payload));
};