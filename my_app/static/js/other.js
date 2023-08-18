$(document).ready(function () {



  var csrfToken = $('[name=csrfmiddlewaretoken]').val();
  $.ajax({
    // url: '/getPosts',
    url: '/probar',
    type: 'POST',
    data: {pagina:'ejemplo'},
    dataType: 'json', // Opcional, dependiendo del tipo de respuesta esperado
    beforeSend: function(xhr) {
        // Agregar el token CSRF a la cabecera de la solicitud
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    },
    success: function(data) {
        // Callback function para manejar la respuesta del servidor
        // data contiene la respuesta del servidor
        // console.log(data.nombre[0]);

        card= $('.list-group')
        var template = ``
        

        for (let i = 0; i < Object.keys(data.nombre).length; i++) {
          const nombre = data.nombre[i];
          const contenido = data.contenido[i];
          template += `
           
            <ul class="list-group list-group-flush ">
              <li class="list-group-item">`+(i+1)+`. `+nombre+`: <a href="">`+contenido+`</a></li>
            </ul>
          
          `

        }       

        card.html(template)


    },
    error: function(xhr, textStatus, errorThrown) {
        // Función que se ejecuta si la solicitud falla
        console.log(textStatus)
    }
  });
  
  
  
  
  
  
  });