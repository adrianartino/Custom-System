
var opciones = document.getElementById('opcion');
var abiertas = document.getElementById('abiertas');
var nombreEncuesta = document.getElementById('nombre');
var boton = document.getElementById('generarPreguntas');
var btnGuardar = document.getElementById('botonGuardar');

var preguntasOpcion = document.getElementById('pregOpcion');
var preguntasAbiertas = document.getElementById('pregAbiertas');



function generadorPreguntas(){
    var cantidadPreguntasOpcion = parseInt(opciones.value);
    var cantidadPreguntasAbierta = parseInt(abiertas.value);
    var contenido ="";
    var contenido2 ="";
    var pregunta = "";
    var preguntaAbierta = "";
    
   //alert(cantidades);
   for (let pregOpcion = 0; pregOpcion < cantidadPreguntasOpcion; pregOpcion++) {
    // Se ejecuta 5 veces, con valores del paso 0 al 4.
    var contador = pregOpcion +1;
    var contadorTexto = contador.toString();
   pregunta = "pregunta" + contadorTexto;
   contenido = contenido + '<div class="col-md-12"><label for="email_address"><span style="color: #078F68;">* </span>Pregunta multiple '+ contadorTexto +':</label><div class="input-group"><span class="input-group-addon"><i class="material-icons">question_answer</i></span><div class="form-line"><input type="text" class="form-control date" id="opcion" placeholder="Ingresar # Preguntas" maxlength="600"  name="'+ pregunta + '" required> </div></div></div>';
  }
   preguntasOpcion.innerHTML = contenido; 

   //alert(cantidades);
   for (let pregOpcion = 0; pregOpcion < cantidadPreguntasAbierta; pregOpcion++) {
    // Se ejecuta 5 veces, con valores del paso 0 al 4.
    var contador2 = pregOpcion +1;
    var contadorTexto2 = contador2.toString();
    preguntaAbierta = "preguntaAb" + contadorTexto2;
   contenido2 = contenido2 + '<div class="col-md-12"><label for="email_address"><span style="color: #078F68;">* </span>Pregunta abierta '+ contadorTexto2 +':</label><div class="input-group"><span class="input-group-addon"><i class="material-icons">question_answer</i></span><div class="form-line"><input type="text" class="form-control date" id="opcion" placeholder="Ingresar # Preguntas" maxlength="600"  name="'+ preguntaAbierta + '" required> </div></div></div>';
  }
   preguntasAbiertas.innerHTML = contenido2; 

   nombreEncuesta.setAttribute('readonly', true);
   opciones.setAttribute('readonly', true);
   abiertas.setAttribute('readonly', true);
   boton.style.display = "none";
  
   btnGuardar.innerHTML = '<button type="submit"class="btn btn-warning m-t-15 waves-effect animate__animated animate__flipInX"  id="generarPreguntas" ><i class="material-icons">laptop_mac</i> Guardar encuesta</button>';
}

