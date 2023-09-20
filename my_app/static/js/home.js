$(document).ready(function () {




  // Oculta elementos <li> después del número máximo de elementos visibles
  

  var url = '/evidence';
  let pausar = false; // Inicialmente, el proceso está activo
  let evidenceIndex; // Índice para recorrer las evidencias
  let id_carrer;
  let maxVisibleItems = 5; // Cambia este valor al número deseado de elementos visibles
  var csrfToken = $('[name=csrfmiddlewaretoken]').val();
  let careers;

  function showEvidenceInHTML(data,i){
    
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

  async function sendFiles() {//Envía las respuesta de imagenes, o vinculo para luego ser enviada al profesor
    
    var fileList = $("#file")[0].files;
    var selectedFiles = [];
    for (var i = 0; i < fileList.length; i++) {
      selectedFiles.push(fileList[i]);
    }
  
    var url_vinculo=$("#vinculo").val()


    tareaIds=$("#tarea_id").val()
    var formData = new FormData();
    
  
    if(fileList.length>0){
      if (selectedFiles.length > 0) {
        for (var i = 0; i < selectedFiles.length; i++) {
          formData.append("files[]", selectedFiles[i]);
        }
      }else if(selectedFiles.length == 0){
        formData.append("files[]", selectedFiles[0]);
      }
    }
    
  
    formData.append("vinculo",url_vinculo)
    formData.append("tarea_id",tareaIds)
    
    console.log('careers');
    try {
  
      const findPost=await $.ajax({
        url: "/findPost",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        beforeSend: function (xhr) {
          // Agregar el token CSRF a la cabecera de la solicitud
          xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
      });

      if(findPost){
        //Cuando se termine el proceso de poner los datos en evidencias, se reanuda el proceso de ir buscando post por post
          if(findPost.status === 200){
            $('#alertSuccess').show()
          }else{
            $('#alertDecline').show()
          }
          // pausar=false
          // GetEvidenceById(careers,evidenceIndex+1)
        
      }

      
  
    } catch (error) {
      console.log("Error:"+ error);
    }
  
    
  
  
  }
  
  async function GetCarrer() {//Obtiene todos los programas o carreras de la cuenta SENA

    try {

      const getCareer = await $.ajax({
        url: url,
        type: 'POST',
        data: {career:1},
        dataType: 'json',
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
        
      });
  
      if (getCareer.id_career && getCareer.title){

        id_carrer=getCareer.id_career
        title=getCareer.title


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
                  <button class="showHomeworks card-link btn btn-light" style="display:none;">Ver + tareas</button>
                  <a href="#" class="card-link btn btn-warning">Ver curso</a>
                </div>
              </div>
            `
            
             
            
          }

          card.html(template_card)

          // Manejador de clic en el botón "Mostrar más"
          $(".showHomeworks").eq(0).on("click", async function() {
            // Muestra los siguientes elementos ocultos
            console.log('Seleccionado el primero y no el segundo');
            var ul = $(".list-group");
            cantItemsShow=3
            ul.find("li:hidden:lt("+cantItemsShow+")").show();
            evidenceIndex=1
            maxVisibleItems=cantItemsShow+maxVisibleItems //3+5=8  8+3=11
            console.log(maxVisibleItems);
          });

          GetAllNumberPosts(id_carrer)
          
        }

        
      }

      
    } catch (error) {
      console.log("Hay un error al enviar datos"+error);
    }

  }

  async function GetAllNumberPosts(id_carrer){//Obtiene todos los numeros POST del curso o carrera, buscando cada evidencia para luego ser agregados en un tag ul

    //Aqui inicia la ultima solicitud, que es para rellenar dato por dato de evidencias
    try {
        
        // Aqui se obtienen todos los numeros POST del curso o carrera
        const career_numbers = await $.ajax({
          url: url,
          type: 'POST',
          data: {id_career: id_carrer[0]},
          dataType: 'json',
          beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
          }
        });
        careers=career_numbers
        GetEvidenceById(career_numbers,0)

    } catch (error) {
      console.log("Error en la solicitud AJAX 3:"+ error.message);
    }
 
  }

  async function GetEvidenceById(career_numbers,index){

    if (career_numbers.id_tareas) {
      totalEvidenceIndex=career_numbers.id_tareas.length
      
          try {

            for (let i = index; i < career_numbers.id_tareas.length; i++) {

              evidenceIndex=i
      
              var id_tarea = career_numbers.id_tareas[i];

              const evidence = await $.ajax({//Se agrega evidencia por evidencia en un tag ul
                url: url,
                type: 'POST',
                data: {id_tareas: id_tarea},
                dataType: 'json',
                beforeSend: function(xhr) {
                  xhr.setRequestHeader('X-CSRFToken', csrfToken);
                }
              });
              // console.log(evidence);
              
              if(evidence){
                // Encuentra el elemento <ul> con el atributo data-career-id coincidente
                var ulCarrer = $('ul[data-career-id="' + evidence.data_evidence[0].id_classroom + '"]');
                if (ulCarrer.length > 0) {
                  // Crea un nuevo elemento <li> para la materia y agrega el texto
                  var evidenceAppend=showEvidenceInHTML(evidence.data_evidence[0],i+1)
    
                  // Agrega el <li> al <ul>
                  ulCarrer.append(evidenceAppend);
        
                }
            
                var ul = $(".list-group"); // Selecciona tu lista <ul>
                ul.find("li:gt(" + (maxVisibleItems - 1) + ")").hide()
                if(evidenceIndex >= maxVisibleItems){
                  restante=(evidenceIndex+1)-maxVisibleItems
                  console.log(restante); //5-2=3
                  $(".showHomeworks").show();
                  
                }
              }

              if (pausar) {
                break;
              }

            }            

            if (pausar) {
              sendFiles()
            }       
            
          } catch (error) {
            console.log(error);
          }

    } else {
      console.log('No hay evidencias, error 3');
    }

  }

  //Utiliza la delegación de eventos para manejar los clics en ".list-group-item a"
$(document).on("click", ".list-group-item a", function (e) {
  e.preventDefault();
  
  var dataInfo = $(this).data('info');
  var tarea_id = $(this).data('tarea-id');
  
  $("#teacher_title").html('<span class="title_card">Profesor: </span>' + dataInfo.profesor);
  $("#work_title").html('<span class="title_card">Materia: </span>' + dataInfo.materia);
  $("#tarea_id").val(tarea_id);

});

 // Manejador de clic en el botón "sendImage"
 $(document).on("click", "#sendImage", async  function (e) {
    e.preventDefault();

    //Cambia de estado la variable pausar, para el bucle de GetAllNumberPosts()
    // pausar = true
    sendFiles()

});



// Inicia el proceso cuando se carga la página, si no está pausado inicialmente
  // GetCarrer();





});










  
  
  

  

