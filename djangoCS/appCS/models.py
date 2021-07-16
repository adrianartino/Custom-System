from django.db import models

# Create your models here.
class Areas (models.Model):
    id_area=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)

    def __str__(self):
        return self.id_area

class Empleados(models.Model):
    id_empleado=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    apellidos=models.CharField(max_length=80)
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)
    puesto=models.CharField(max_length=80)
    correo=models.EmailField(max_length=80)
    contraseña=models.CharField(max_length=40, null=True)
    activo=models.CharField(max_length=2)


    def __str__(self):
        return self.id_empleado

class Equipos (models.Model):
    id_equipo=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=80)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    color=models.CharField(max_length=80)
    imagen=models.ImageField(upload_to="imagenesequipos", null = True)
    memoriaram=models.CharField(max_length=80)
    procesador=models.CharField(max_length=80)
    sistemaoperativo=models.CharField(max_length=80)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    estado=models.CharField(max_length=80)
    activo=models.CharField(max_length=2)

    def __str__(self):
        return self.id_equipo

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
        return self.id_impresora

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
    operacion=models.CharField(max_length=80)
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
    operacion=models.CharField(max_length=80)
    fecha_hora=models.DateTimeField()
