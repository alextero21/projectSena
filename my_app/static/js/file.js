$(document).ready(function () {

  //Es el boton adjuntar un vinculo
  $($(".color5")[0]).click(function (e) { 
    // e.preventDefault();
    $("#subeLtare").css("display","block")
    $("#subeLtare").html(`<input type="text" size="50" id="linktare" style="width:405px; margin-right:5px; height:23px; border:1px solid #ccc;">
    <a class="color5" id="botonC" style="text-decoration:none; margin-right:10px;">Cancelar</a><a class="color2" id="botonL" style="text-decoration:none;">Adjuntar</a>`)
    
    // $("#subeLtare").html('Vínculo agregado: <span>'+$("#linktare").val()+'</span>')
    $("#botonC").click(function (e) { 
      // e.preventDefault();
      $("#subeLtare").css("display","none")
      
    });
    
  });




  
  

  // $("#vinculos").click(function (e) { 
  //   // e.preventDefault();
  //   $("#subeLtare").html(`<input type="text" size="50" id="linktare" style="width:405px; margin-right:5px; height:23px; border:1px solid #ccc;"><a class="color5" id="botonC" href="javascript:cancelarLinkTarea();" style="text-decoration:none; margin-right:10px;">Cancelar</a><a class="color2" id="botonL" style="text-decoration:none;">Adjuntar</a>`)
  
  //   $("#botonL").click(function (e) { 
  //     // e.preventDefault();
  
  //     $("#subeLtare").html('Vínculo agregado: <span>'+$("#linktare").val()+'</span>')
      
  //   });
  // });

  

  var selectedFiles = [];
  $("#file").change(function() {
    var fileInput = this;
    var imageContainer = $("#imageContainer");


    for (var i = 0; i < fileInput.files.length; i++) {
      var file = fileInput.files[i];
      var reader = new FileReader();

      selectedFiles.push(fileInput.files[i]);
      $("#ullista").append("<br>" + fileInput.files[i].name);

      reader.onload = function(event) {
        var image = document.createElement("img");
        image.src = event.target.result;
        image.className = "uploaded-image";
        imageContainer.append(image);
      };

      reader.readAsDataURL(file);
    }
  });


  $("#contestarTareaBoton").click(function (e) { 
    var texto_vinculo = $("#linktare").val();


    var formData = new FormData();
    formData.append("textData", texto_vinculo); // Agregar texto al FormData
    if (selectedFiles.length > 0) {
      for (var i = 0; i < selectedFiles.length; i++) {
        formData.append("files[]", selectedFiles[i]);
      }
    }else if(selectedFiles.length == 0){
      formData.append("files[]", selectedFiles[0]);
    }
      
    console.log(formData);
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: "/file",
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      beforeSend: function(xhr) {
        // Agregar el token CSRF a la cabecera de la solicitud
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
       },
      success: function(response) {
        console.log("Éxito:", response);
      },
      error: function(error) {
        console.log("Error:", error);
      }
    });
    
  });
  

  

  // <div class="color5" id="subeLtare" style="display: block; padding: 4px; font-size: 13px;"><input type="text" size="50" id="linktare" style="width:405px; margin-right:5px; height:23px; border:1px solid #ccc;"><a class="color5" id="botonC" href="javascript:cancelarLinkTarea();" style="text-decoration:none; margin-right:10px;">Cancelar</a><a class="color2" id="botonL" href="javascript:pathLinkTarea()" style="text-decoration:none;">Adjuntar</a></div>

});