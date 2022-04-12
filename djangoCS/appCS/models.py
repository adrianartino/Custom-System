from os import truncate
from pyexpat import model
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import CharField


# Create your models here.
class Areas (models.Model):
    id_area=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    color=models.CharField(max_length=80)

    def __str__(self):
        return str(self.id_area())

class Empleados(models.Model):
    id_empleado=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    apellidos=models.CharField(max_length=80)
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)
    puesto=models.CharField(max_length=80)
    correo=models.EmailField(max_length=80)
    contraseña=models.CharField(max_length=40, null=True)
    imagen_empleado=models.ImageField(upload_to="empleados", null = True)
    activo=models.CharField(max_length=2)


    def __str__(self):
        return str(self.id_empleado())

class Equipos (models.Model):
    id_equipo=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=80)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    color=models.CharField(max_length=80)
    imagen=models.ImageField(upload_to="imagenesequipos", null = True)
    pdf=models.FileField(upload_to='pdfequipos', null=True)
    memoriaram=models.CharField(max_length=80)
    procesador=models.CharField(max_length=80)
    sistemaoperativo=models.CharField(max_length=80)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    estado=models.CharField(max_length=80)
    activo=models.CharField(max_length=2)
    modelocargador=models.CharField(max_length=80, null=True)
    fechaMant=models.DateField(null=True)

    def __str__(self):
        return self.id_equipo

class Mouses (models.Model):
    id_mouse = models.AutoField(primary_key=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="mouses", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_mouse

class Teclados (models.Model):
    id_teclado = models.AutoField(primary_key=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="teclados", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_teclado

class Monitores (models.Model):
    id_monitor = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="monitores", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_monitor

class Telefonos (models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados,  on_delete=models.CASCADE, null=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="telefonos", null = True)
    extension = models.CharField(max_length=10, null=True)
    nodo = models.CharField(max_length=20, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_telefono



class Renovacion_Equipos (models.Model):
    id_renov_equipo=models.AutoField(primary_key=True)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    fecha_compra=models.DateField()
    fecha_renov=models.DateField()
    

     

class Carta (models.Model):
    id_carta=models.AutoField(primary_key=True)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    fecha=models.DateField()
    firma=models.ImageField(upload_to="firmas", null = True)
    


class Impresoras (models.Model):
    id_impresora=models.AutoField(primary_key=True)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    numserie=models.CharField(max_length=80)
    imagen=models.ImageField(upload_to="impresoras", null = True)
    tipo=models.CharField(max_length=80)
    enred=models.CharField(max_length=2)
    ip=models.CharField(max_length=16, null=True)
    estado=models.CharField(max_length=80)
    activo=models.CharField(max_length=2)
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_impresora)
    
class Renovacion_Impresoras (models.Model):
    id_renov_imp=models.AutoField(primary_key=True)
    id_impresora=models.ForeignKey(Impresoras,on_delete=CASCADE)
    fecha_compra=models.DateField()
    fecha_renov=models.DateField()

class Cartuchos (models.Model):
    id_cartucho=models.AutoField(primary_key=True)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    cantidad=models.IntegerField()
    nuserie=models.CharField(max_length=10)
    color=models.CharField(max_length=80)
    imagenCartucho=models.ImageField(upload_to="cartuchos", null = True)
    id_impresora=models.ForeignKey(Impresoras, on_delete=models.CASCADE)

class CalendarioMantenimiento (models.Model):
    id_calmantenimiento=models.AutoField(primary_key=True)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE,null=True)
    id_impresora=models.ForeignKey(Impresoras, on_delete=models.CASCADE,null=True)
    operacion=models.CharField(max_length=200)
    fecha=models.DateField()
    observaciones=models.CharField(max_length=100)

class Programas (models.Model):
    id_programa=models.AutoField(primary_key=True)
    nombre_version=models.CharField(max_length=80)
    tipo=models.CharField(max_length=80)
    licencia=models.CharField(max_length=80)
    idioma=models.CharField(max_length=80)
    sistemaoperativo_arq=models.CharField(max_length=80)
    memoria_ram=models.CharField(max_length=80)
    procesador=models.CharField(max_length=80)
    imagenPrograma=models.ImageField(upload_to="programas", null = True)

    def __str__(self):
        return self.id_programa

class ProgramasArea (models.Model):
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)
    id_programa=models.ForeignKey(Programas, on_delete=models.CASCADE)

class EquipoPrograma (models.Model):
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    id_programa=models.ForeignKey(Programas, on_delete=models.CASCADE)

class Bitacora (models.Model):
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE)
    tabla=models.CharField(max_length=80)
    id_objeto=models.IntegerField()
    operacion=models.CharField(max_length=80)
    fecha_hora=models.DateTimeField()
    
class Encuestas (models.Model):
    id_encuesta = models.AutoField(primary_key=True)
    fecha_encuesta = models.DateField()
    nombre_encuesta = models.CharField(max_length=80)
    preguntas_multiples = models.CharField(max_length=80)
    preguntas_abiertas = models.CharField(max_length=80)
    def __str__(self):
        return self.id_encuesta
        
class Preguntas (models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    id_encuesta = models.ForeignKey(Encuestas, on_delete=models.CASCADE)
    pregunta = models.TextField(max_length=500)
    tipo = models.CharField(max_length=3)
    clasificacion = models.CharField(max_length=100)
    def __str__(self):
        return self.id_pregunta
    

class Respuestas (models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    respuesta = models.TextField(max_length=100)

  

class EncuestaEmpleadoResuelta (models.Model):
    id_empleado = id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_encuesta = models.ForeignKey(Encuestas, on_delete=models.CASCADE)

class DiscosDuros (models.Model):
    id_disco = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=30)
    marca = models.CharField(max_length=30)
    capacidad = models.IntegerField(null=True)
    dimension = models.CharField(max_length=20)
    alm_uso = models.IntegerField(null=True)
    alm_libre = models.IntegerField(null=True)
    estado = models.CharField(max_length=30)
    def __str__(self):
        return self.id_disco

class EmpleadosDiscosDuros (models.Model):
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_disco = models.ForeignKey(DiscosDuros, on_delete=models.CASCADE)
    fecha = models.DateField(null=True)

class MemoriasUSB (models.Model):
    id_usb = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    capacidad = models.IntegerField()
    cantidadStock = models.IntegerField()
    def __str__(self):
        return self.id_usb


class PrestamosSistemas (models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    tabla = models.CharField(max_length=100, null=True)
    id_producto = models.CharField(max_length=4, null=True)
    otro = models.CharField(max_length=100, null=True)
    cantidad = models.IntegerField()
    fecha_prestamo = models.DateField()
    firma_entrega = models.ImageField(upload_to="firmasPrestamos", null = True)
    devolucion = models.CharField(max_length=1)
    fecha_entrega = models.DateField(null=True)
    condiciones = models.CharField(max_length=100, null=True)
    firma_devolucion = models.ImageField(upload_to="firmasPrestamos2", null = True)
    estatus = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.id_prestamo
    
class SoportesTecnicos (models.Model):
    id_soporte = models.AutoField(primary_key = True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_soporte = models.DateField()
    equipo_soporte = models.CharField(max_length=50, null=True)
    tabla = models.CharField(max_length=100)
    operacion = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=250, null=True)
    resuelto_interno = models.CharField(max_length=2, null=True)
    resuelto_proveedor = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.id_soporte
    
    
class ImplementacionSoluciones (models.Model):
    id_implementacion = models.AutoField(primary_key = True)
    titulo_problema = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    fecha_comienzo = models.DateField()
    fecha_terminada = models.DateField()
    resuelto = models.CharField(max_length=2)
    revisado = models.CharField(max_length=2)
    firma_direccion = models.ImageField(upload_to="firmasImplementaciones", null = True)
    comentarios_direccion =  models.CharField(max_length=250, null=True)
    
    
    def __str__(self):
        return self.id_implementacion
