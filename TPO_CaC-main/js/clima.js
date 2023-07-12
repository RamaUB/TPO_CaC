// Fetch para obtener datos para completar el clima.
(function(){
    fetch('https://api.weatherbit.io/v2.0/current?lat=-34.6131&lon=-58.3772&lang=es&key=d71ef4a704e8411db65e86cfbf5d796f')
        .then(data => data.json())
        .then(data => {
            console.log(data.data[0])
            climaAhora(data.data[0])
        })
})()

//funcion para crear los elementos y cargar la info del clima en el html 
function climaAhora(clima){
    let ubicacion = document.createElement("h2");
    let tiempo = document.createElement("img");
    let temperatura = document.createElement("p");

    ubicacion.textContent = "Hoy en " + clima.city_name;
    tiempo.src = "https://cdn.weatherbit.io/static/img/icons/"+clima.weather.icon+".png"
    temperatura.textContent = `${clima.weather.description} y ${clima.app_temp}°C`;

    let cajaClima = document.querySelector("#clima");
    cajaClima.appendChild(ubicacion);
    cajaClima.appendChild(tiempo);
    cajaClima.appendChild(temperatura);
}




