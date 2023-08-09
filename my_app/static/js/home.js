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


//   form = formSerialize();
//   page = (page) ? page : 1;
//   dataAjax = form + "&limit=" + limitSearch + "&offset=" + page;
//   form.limit = limitSearch;
//   form.offset = page;
//   var dataSend = 'method=' + method + '&param=' + JSON.stringify(form);
  
//   $.ajax({
//     type: "POST",
//     url: urlSearch,
//     dataType: "json",
//     data: dataSend,
//     success: function(data) {
//      console.log(data);
//     },
//     error: function(xhr, textStatus, errorThrown) {
//         console.log("Error:", xhr);
//     }
// });


function sendAjax(){
  idgrupo=31247202
  dataAjax = "methodclave=registroclave&idgrupo="+idgrupo;
  //alert(dataAjax);
  $.ajax({
                    type:'POST',
                    url:'https://sena.territorio.la/webservices/grupo.php',
                    data: dataAjax,
                    cache: false,
                    success:function(response) {
  
                       // console.log(response);
                        //alert(response);
  
                        console.log(response);
                    },
                    error: function(xhr) {
                      //alert('error');
                    }
    });
}

$('#presiona').click(function (e) { 
  e.preventDefault();
  sendAjax()
});







});