# Generated by Django 4.0.4 on 2022-05-27 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0033_remove_celulares_fecha_contratacion_plan_final_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartaCelular',
            fields=[
                ('id_carta_celular', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('firma', models.ImageField(null=True, upload_to='firmasCartaCelular')),
                ('id_celular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.celulares')),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCS.empleados')),
            ],
        ),
    ]
