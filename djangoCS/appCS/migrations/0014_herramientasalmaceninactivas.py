# Generated by Django 4.0.3 on 2022-04-26 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0013_herramientasalmacen_tipo_herramienta'),
    ]

    operations = [
        migrations.CreateModel(
            name='HerramientasAlmacenInactivas',
            fields=[
                ('id_herramientaInactiva', models.AutoField(primary_key=True, serialize=False)),
                ('motivo_baja', models.CharField(max_length=6)),
                ('explicacion_baja', models.TextField()),
                ('cantidad_baja', models.CharField(max_length=15, null=True)),
                ('fecha_baja', models.DateField()),
                ('id_herramienta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.herramientasalmacen')),
                ('id_prestamo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appCS.prestamosalmacen')),
            ],
        ),
    ]
