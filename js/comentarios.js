// Fetch para obtener datos para completar la sección comentarios.
(function (){
    let numeroAzar = Math.floor(Math.random() * 100);
    const requestURL = `https://jsonplaceholder.typicode.com/posts/${numeroAzar}/comments`;
    fetch(requestURL)
        .then(data => data.json())
        .then(data => {
            //console.log(data.length)
            let caja = document.querySelector("#cajaComentarios");
            let i;
            for (i=0; i<data.length; i++){
                caja.appendChild(publicarComentario(data[i],i));
            }
            })
})()

//función para crear los elementos en el html y cargar la información obtenida de la api.
function publicarComentario(comentario,i){
    let div = document.createElement("div");
    let clase = (i % 2 == 0)? "comentarioDerecha" : "comentarioIzquierda";
    div.classList = clase;
    let nombre = document.createElement("h2");
    nombre.textContent = comentario.name + ' dice: ';
    div.appendChild(nombre);
    let mail = document.createElement("p");
    mail.textContent = 'E-mail: '+comentario.email;
    div.appendChild(mail);
    let texto = document.createElement("p");
    texto.textContent = '"' + comentario.body+ '"';
    div.appendChild(texto);

    return div;
}