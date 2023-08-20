$(document).ready(function () {

    var selectedFiles = [];
    $("#file").change(function() {
      var fileInput = this;


      for (var i = 0; i < fileInput.files.length; i++) {
        selectedFiles.push(fileInput.files[i]);
      }

      // console.log(selectedFiles);
    });

    
    

  
    $("#sendImage").click(function (e) { 
      // e.preventDefault();
      var texto_vinculo = $("#vinculo").val();
      var formData = new FormData();
      formData.append("vinculo",texto_vinculo)

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
        url: "/test",
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
        error: function(xhr, textStatus, errorThrown) {
          console.log("Error:", textStatus);
        }
      });

    });

    


});