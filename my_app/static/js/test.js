$(document).ready(function() {
  var contenedor = $("#contenedor");
  var boton = $("#verMas");
  var divsAgregados = 0;
  var activar = false;
  

  boton.click(function() {

    if(activar==false){
      var numeroAleatorio = Math.floor(Math.random() * 99999999) + 1;
      // Simulación de contenido para el nuevo div
      var nuevoContenido = "Contenido del div " + (divsAgregados + 3);
  
      var nuevoDiv = $("<div>").attr("id", "post["+numeroAleatorio+"]").text(nuevoContenido);
      contenedor.append(nuevoDiv);
  
      divsAgregados++;
    }
    

    if (divsAgregados >= 4) {
      activar=true
    }
  });
});
