

var empleados = document.getElementById('numeroEmpleados');

var boton = document.getElementById('generarEmpleados');
var btnGuardar = document.getElementById('botonGuardar');


var respaldos = document.getElementById('empleadosDiscos');



function generadorEmpleados(){
    var cantidadEmpleados = parseInt(empleados.value);
  
    var contenido ="";
    var empleado ="";
   
 
    
   //alert(cantidades);
   for (let empleados = 0; empleados < cantidadEmpleados; empleados++) {
    // Se ejecuta 5 veces, con valores del paso 0 al 4.
    var contador = empleados +1;
    var contadorTexto = contador.toString();
    empleado = "empleado" + contadorTexto;
   
   contenido = contenido + ' <div class="col-md-12"><label for="email_address"><span style="color: #bcc0bf;">* </span>Empleado '+ contadorTexto +': </label><div class="input-group"><span class="input-group-addon"><i class="material-icons">account_box</i></span><select class="form-control show-tick" name="' + empleado + '">{% for empleado in empleados %}<option value="{{empleado.id_empleado}}">{{empleado.nombre}} {{empleado.apellidos}}</option>{% endfor %}</select></div></div>';
  }
   respaldos.innerHTML = contenido; 

   

  

  
   empleados.setAttribute('readonly', true);

   boton.style.display = "none";
  
   btnGuardar.innerHTML = ' <button type="submit" class="btn bg-indigo m-t-15 waves-effect animate__animated animate__flipInX"><i class="material-icons">save</i> Agregar disco duro</button>';
}