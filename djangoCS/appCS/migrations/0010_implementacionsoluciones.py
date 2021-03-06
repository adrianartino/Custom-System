# Generated by Django 3.2.5 on 2022-04-12 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0009_auto_20220412_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImplementacionSoluciones',
            fields=[
                ('id_implementacion', models.AutoField(primary_key=True, serialize=False)),
                ('titulo_problema', models.CharField(max_length=250)),
                ('descripcion', models.CharField(max_length=250)),
                ('fecha_comienzo', models.DateField()),
                ('fecha_terminada', models.DateField()),
                ('resuelto', models.CharField(max_length=2)),
                ('revisado', models.CharField(max_length=2)),
                ('firma_direccion', models.ImageField(null=True, upload_to='firmasImplementaciones')),
                ('comentarios_direccion', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]
