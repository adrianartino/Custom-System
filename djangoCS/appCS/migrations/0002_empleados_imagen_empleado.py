# Generated by Django 3.2.5 on 2021-09-03 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados',
            name='imagen_empleado',
            field=models.ImageField(null=True, upload_to='empleados'),
        ),
    ]