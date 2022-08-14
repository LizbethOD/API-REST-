function get_Clientes(){

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    
    var request = new XMLHttpRequest();

    request.open("GET","https://8000-lizbethod-apirest-n3l0fmlt2en.ws-us60.gitpod.io/user/autenticacion/",true);
    request.setRequestHeader("Authorization", "Basic " + btoa(email + ":" + password));
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept","application/json");
    
    request.onload = () =>{
        const response = request.responseText;
        const status = request.status
        const data = JSON.parse(response);

        if (status == 202) {
            alert("Hola, Bienvenido");
            sessionStorage.setItem("item",data.token);
            window.location.replace("get_clientes.html");
            console.log(data.token)
        }
        else{
            alert("Ups! Datos incorrectos, vuelve a revisar tus datos:)");
        }
    };
   request.send();
};