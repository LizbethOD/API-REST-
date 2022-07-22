function postCliente(){

    var request = new XMLHttpRequest();

    username = prompt('Username:')
    password = prompt('Password:')

    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");
    let payload = {
        "nombre": nombre.value,
        "email" : email.value,
    }

    console.log("nombre: " + nombre.value);
    console.log("email: "  + email.value);
    console.log(payload);
    
    request.open('POST', "https://8000-lizbethod-apirest-h5fixnrf1oq.ws-us54.gitpod.io/clientes/",true);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))

    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response);     
        const status    = request.status;

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