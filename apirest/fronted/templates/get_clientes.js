function get_Clientes(){

    var token = sessionStorage.getItem('item');
    console.log(token);
    var request = new XMLHttpRequest();

    request.open("GET","https://8000-lizbethod-apirest-n3l0fmlt2en.ws-us60.gitpod.io/clientes/",true);
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("Accept","application/json")
    
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);

        var tbody = document.getElementById("tbody");
        for(let row=0; row<json.length; row++){
            var tr = document.createElement("tr");
            var id_cliente = document.createElement("td");
            var nombre_cliente = document.createElement("td");
            var email_cliente = document.createElement("td");
            var detalle_cliente = document.createElement("td");
            var actualizar_cliente = document.createElement("td");
            var eliminar_cliente = document.createElement("td");

            id_cliente.innerHTML = json[row].id_cliente;
            nombre_cliente.innerHTML = json[row].nombre;
            email_cliente.innerHTML = json[row].email;
            detalle_cliente.innerHTML = "<a href='/templates/get_cliente.html?"+json[row].id_cliente+"'>Detalle</a>";
            actualizar_cliente.innerHTML =  "<a href='/templates/put_cliente.html?"+json[row].id_cliente+"'>Actualizar</a>";
            eliminar_cliente.innerHTML =  "<a href='/templates/delete_cliente.html?"+json[row].id_cliente+"'>Eliminar</a>";

            tr.appendChild(id_cliente);
            tr.appendChild(nombre_cliente);
            tr.appendChild(email_cliente);
            tr.appendChild(detalle_cliente);
            tr.appendChild(actualizar_cliente);
            tr.appendChild(eliminar_cliente);
            tbody.appendChild(tr);
        }
    };
    request.send();
};