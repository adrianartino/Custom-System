from django.db import models

# Create your models here.
class Empleados(models.Model):
    id_empleado=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    apellidos=models.CharField(max_length=80)
