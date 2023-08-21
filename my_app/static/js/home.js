document.addEventListener('DOMContentLoaded', function () {
const slider = document.getElementById('slider');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentSlide = 0;

// Función para avanzar al siguiente slide
function nextSlide() {
  currentSlide++;
  if (currentSlide >= slider.children.length) {
    currentSlide = slider.children.length - 1;
  }
  updateSliderPosition();
}

// Función para retroceder al slide anterior
function prevSlide() {
  

  currentSlide--;
  if (currentSlide < 0) {
    currentSlide = 0;
  }
  updateSliderPosition();
}

// Actualizar la posición del slider para mostrar el slide actual
function updateSliderPosition() {
  const slideWidth = slider.children[0].clientWidth;
  const newPosition = -currentSlide * slideWidth;
  slider.style.transform = `translateX(${newPosition}px)`;

  // Mostrar u ocultar las flechas según la posición actual del slider
  prevBtn.style.display = currentSlide === 0 ? 'none' : 'block';
  nextBtn.style.display = currentSlide === slider.children.length - 1 ? 'none' : 'block';
}

// Eventos para los botones de flecha
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

// Iniciar el slider
updateSliderPosition();
});
// Puedes agregar funciones para hacer el slider automático si lo deseas
// por ejemplo, utilizando setInterval para llamar a nextSlide automáticamente cada cierto tiempo.







var uni = 1256;
//var cmp = 1;
var pers = 26182335;



var urlSearch = "/webservices/academico.php";
var mainContent = "catalogo-main-content";
var method = "obtenerMateriasConPaginacion";
var totalPages = 0;
var rangePages = 20;
var limitSearch = 100;
var idUniversidad = "1256";
var idPersona = "26182335";
//grupos donde esta inscrito 
var valueTab = 5;

$(document).ready(function () {

  // var objetjson= [
  //   {'name':'alex', 
  //   'age':47,
  //   'city':['London', 'Paris', 'Sao paulo' ]
  //   },
  //   {'name':'camilo'}
  // ]

  // console.log(objetjson);



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

      console.log(data);
        // // Callback function para manejar la respuesta del servidor
        // // data contiene la respuesta del servidor

        // card= $('#card')
        // var template_card = ``
        
        // for (let i = 0; i < data.data.length; i++) {

        //   var d=data.data[i]
        //   // console.log(d.id_tarea);
        //   // console.log(d);
         

        //   var content = ``
        //   for (let e = 0; e < d.names.length; e++) {
            
        //     var nombre = d.names[e];
        //     var contenido = d.content[e];
        //     var id_tarea = d.id_tarea[e];
        //     var materia = d.materia[e];
        //     // console.log(tarea);
        //     // var classroom = arrayData.classroom;
        //     // data-id-tarea=`+d.id_tarea+`
        //     content+=`
        //       <li class="list-group-item">`+(e+1)+`. `+nombre+`: <a data-bs-toggle="modal" data-bs-target="#exampleModal" href="" data-tarea-id="`+id_tarea+`" data-info='{"profesor": "`+nombre+`", "materia": "`+materia+`"}'>`+contenido+`</a></li>
        //     `
        //     // titulo_curso+=classroom
        //   }

          
        //   template_card += `
        //     <div class="card decoration_card" style="width: 18rem;">
        //       <img src="../static/images/agente.png" class="card-img-top" alt="...">
        //       <div class="card-body">
        //         <h5 class="card-title ">`+d.classroom+`</h5>
        //         <p class="card-text">Recorderis: sadsadasd</p>
        //       </div>
        //       <ul class="list-group list-group-flush ">
        //         `+content+`
        //       </ul>
              
        //       <div class="card-body decoration_card">
        //         <a href="#" class="card-link btn btn-light">Todas las tareas</a>
        //         <a href="{{'getUrl'}}{{e.href}}" class="card-link btn btn-warning">Ver curso</a>
        //       </div>
        //     </div>
        //   `
        // }       



        // card.html(template_card)

        // $(".list-group-item a").click(function (e) {//Este es cuando se abre el post 
        //   // e.preventDefault();
          
        //   var dataInfo = $(this).data('info')
        //   var tarea_id = $(this).data('tarea-id')
          
        //   $("#teacher_title").html('<span class="title_card">Profesor: </span>'+dataInfo.profesor)
        //   $("#work_title").html('<span class="title_card">Materia: </span>'+dataInfo.materia)
          
        //   $("#sendImage").data('tarea-id', tarea_id);
          
        // });



        // var selectedFiles = [];
        // $("#file").change(function() {
        //   var fileInput = this;
        //   for (var i = 0; i < fileInput.files.length; i++) {
        //     selectedFiles.push(fileInput.files[i]);
        //   }
        // });



        // $("#sendImage").click(function (e) { 
        //   // e.preventDefault();
        //   var url_vinculo=$("#vinculo").val()
        //   var id_tarea=$(this).data('tarea-id')

        //   var formData = new FormData();

        //   if (selectedFiles.length > 0) {
        //     for (var i = 0; i < selectedFiles.length; i++) {
        //       formData.append("files[]", selectedFiles[i]);
        //     }
        //   }else if(selectedFiles.length == 0){
        //     formData.append("files[]", selectedFiles[0]);
        //   }

        //   formData.append("vinculo",url_vinculo)
        //   formData.append("tarea_id",id_tarea)

        //   var csrfToken = $('[name=csrfmiddlewaretoken]').val();
        //   $.ajax({
        //     url: "/findPost",
        //     type: "POST",
        //     data: formData,
        //     contentType: false,
        //     processData: false,
        //     beforeSend: function(xhr) {
        //       // Agregar el token CSRF a la cabecera de la solicitud
        //       xhr.setRequestHeader('X-CSRFToken', csrfToken);
        //     },
        //     success: function(response) {
        //       console.log("Éxito:", response);
        //     },
        //     error: function(error) {
        //       console.log("Error:", error);
        //     }
        //   });

          
          
        //   console.log(id_tarea);
        //   console.log(url_vinculo);
        //   console.log(selectedFiles);
        // });


    },
    error: function(xhr, textStatus, errorThrown) {
        // Función que se ejecuta si la solicitud falla
        console.log(xhr)
        console.log(textStatus)
        console.log(errorThrown)
    }
  });
  
  
  
  

  
  });

  //Tarea: Maria Elena
  //Contexto de la tarea
  //Usar Tailwind-> Titulo, escribir descripcion, subir archivo, enviar evidencia