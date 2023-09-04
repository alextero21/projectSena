

//RELAJATE!!!
// var id_carrer; // Variable global para almacenar el valor de id_carrer


$(document).ready(function () {

  var url = '/probar';
  var pausar = false; // Inicialmente, el proceso está activo
  var evidenceIndex = 0; // Índice para recorrer las evidencias

  function showEvidence(data,i){
    
    var content = ``
    
    var d=data// El array con todos los datos de las evidencias

    var nombre_profesor = d.names;
    var contenido = d.content;
    var id_tarea = d.id_tarea;
    var materia = d.materia;
    var classroom = d.classroom;
    var didHomework = d.didHomework;
    var date_end = d.date_end;

    content+=`
      <li class="list-group-item">`+i+`. `+nombre_profesor+`: <a data-bs-toggle="modal" data-bs-target="#exampleModal" href="" data-tarea-id="`+id_tarea+`" data-info='{"profesor": "`+nombre_profesor+`", "materia": "`+materia+`"}'>`+contenido+`</a></li>
    `
    return content

  }
  
  async function requestEachEvidence() {
    console.log(pausar);
    if (pausar) return; // Si está pausado, no continúes
    console.log('Dentro del EVIDENCE BUCLE');

    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
    try {
      const data = await $.ajax({
        url: url,
        type: 'POST',
        data: {career:1},
        dataType: 'json',
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
      });
  

      if (data.id_career && data.title){


        id_carrer=data.id_career
        title=data.title

        if(id_carrer.length == title.length){
          
          card= $('#card')//El div donde se va a colocar dato por dato

          var template_card = ``
          for (let o = 0; o < id_carrer.length; o++) {
            id_carrer_for = id_carrer[o];
            title_for = title[o];

            template_card += `
              <div class="card decoration_card" style="width: 18rem;">
                <img src="../static/images/agente.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title ">`+title_for+`</h5>
                  <p class="card-text">Recorderis: SIIIIII</p>
                </div>
                <ul class="list-group list-group-flush " data-career-id="`+id_carrer_for+`"></ul>
                
                <div class="card-body decoration_card">
                  <a href="#" class="card-link btn btn-light">Todas las tareas</a>
                  <a href="#" class="card-link btn btn-warning">Ver curso</a>
                </div>
              </div>
            `
            
             
            
          }

          card.html(template_card)
          

          try {//Aqui se obtienen todos los numeros POST del curso o carrera
            const data = await $.ajax({
              url: url,
              type: 'POST',
              data: {id_career: id_carrer[0]},
              dataType: 'json',
              beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
              }
            });
      
        
            if (data.id_tareas) {
      
              for (let i = 0; i < data.id_tareas.length; i++) {
      
                var id_tarea = data.id_tareas[i];
      
                  const evidence = await $.ajax({
                    url: url,
                    type: 'POST',
                    data: {id_tareas: id_tarea},
                    dataType: 'json',
                    beforeSend: function(xhr) {
                      xhr.setRequestHeader('X-CSRFToken', csrfToken);
                    }
                  });
                  // Encuentra el elemento <ul> con el atributo data-career-id coincidente
                  var ulCarrer = $('ul[data-career-id="' + evidence.data_evidence[0].id_classroom + '"]');
      
                  if (ulCarrer.length > 0) {
                    // Crea un nuevo elemento <li> para la materia y agrega el texto
                    var evidenceAppend=showEvidence(evidence.data_evidence[0],i+1)
      
                    // Agrega el <li> al <ul>
                    ulCarrer.append(evidenceAppend);
          
                  }
                
      
      
              }
           
              
            } else {
              console.log('No hay evidencias, error 3');
            }
          } catch (error) {
            console.log("Error en la solicitud AJAX 3:", error);
          }

        }

        
      }

      
    } catch (error) {
      console.log("Hay un error al enviar datos");
    }

    // Incrementa evidenceIndex para obtener la siguiente evidencia en la próxima llamada
    evidenceIndex++;

    // Llama recursivamente a procesarEvidencias después de un retraso (puedes ajustar el tiempo)
    // setTimeout(requestEachEvidence, 20000); // 1000 milisegundos (1 segundo)
  }

  //Utiliza la delegación de eventos para manejar los clics en ".list-group-item a"
$(document).on("click", ".list-group-item a", function (e) {
  e.preventDefault();
  
  var dataInfo = $(this).data('info');
  var tarea_id = $(this).data('tarea-id');
  
  $("#teacher_title").html('<span class="title_card">Profesor: </span>' + dataInfo.profesor);
  $("#work_title").html('<span class="title_card">Materia: </span>' + dataInfo.materia);
  
  $("#sendImage").data('tarea-id', tarea_id);

});

 // Manejador de clic en el botón "sendImage"
 $(document).on("click", "#sendImage", async  function (e) {
  e.preventDefault();
  pausar = true;

  var fileList = $("#file")[0].files;
  var selectedFiles = [];

  for (var i = 0; i < fileList.length; i++) {
    selectedFiles.push(fileList[i]);
  }

  var url_vinculo=$("#vinculo").val()
  var id_tarea=$(this).data('tarea-id')

  var formData = new FormData();

  if (selectedFiles.length > 0) {
    for (var i = 0; i < selectedFiles.length; i++) {
      formData.append("files[]", selectedFiles[i]);
    }
  }else if(selectedFiles.length == 0){
    formData.append("files[]", selectedFiles[0]);
  }

  formData.append("vinculo",url_vinculo)
  formData.append("tarea_id",id_tarea)

  var csrfToken = $('[name=csrfmiddlewaretoken]').val();
  try {

    const responseServer = await $.ajax({
      url: "/findPost",
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      beforeSend: function (xhr) {
        // Agregar el token CSRF a la cabecera de la solicitud
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
      },
      success: function (data) {
      // Aquí puedes manejar la respuesta exitosa del servidor
      
        console.log(data);
        
        // requestEachEvidence();

        

  
      // Puedes realizar acciones adicionales aquí según la respuesta del servidor
    },
    error: function (error) {
      // Aquí puedes manejar errores en la solicitud AJAX
      console.log("Error:"+ error);
    },
    complete: function () {
      // Esta función se ejecutará después de que se complete la solicitud,
      // ya sea exitosa o con error. Puedes realizar acciones generales aquí.
      console.log("COMPLETE:");
      console.log("LISTO PARA EL EVIDENCE:");
      pausar = false;
      // requestEachEvidence()
    }
  
  });
          

  } catch (error) {
    console.log("Error:"+ error);
  }


});

// Inicia el proceso cuando se carga la página, si no está pausado inicialmente
  requestEachEvidence();


});

// const array=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','V','W','X','Y','Z']


// let index = 0;
// let pausar = false; // Inicialmente, el bucle está iniciado

// function letrasAMostrar(array) {
//   if (index < array.length) {
//     const letra = array[index];
//     console.log('Letra: ' + letra);
//     index++;
//   } else {
//     console.log('Fin del array');
//     pausar = true; // Cuando llegamos al final, pausamos el bucle
//   }
  
//   if (!pausar) {
//     setTimeout(function() {
//       letrasAMostrar(array); // Llama a la función recursivamente después de un retraso
//     }, 1000);
//   }
// }

// $(document).on("click", "#enviar", async function (e) {
//   pausar = !pausar; // Cambia el estado de pausa al hacer clic en el botón
//   if (!pausar) {
//     letrasAMostrar(array); // Inicia o reanuda el bucle si no está pausado
//   }
// });

// // Inicia el bucle si no está pausado inicialmente
// if (!pausar) {
//   letrasAMostrar(array);
// }








  
  
  

  

