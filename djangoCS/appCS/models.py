from os import truncate
from django.db import models
from django.db.models.deletion import CASCADE

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
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
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
    respuesta = models.TextField(max_length=600)

class EncuestaEmpleadoResuelta (models.Model):
    id_empleado = id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_encuesta = models.ForeignKey(Encuestas, on_delete=models.CASCADE)