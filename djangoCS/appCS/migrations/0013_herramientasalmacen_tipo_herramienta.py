# Generated by Django 4.0.3 on 2022-04-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0012_herramientasalmacen_cantidad_existencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='herramientasalmacen',
            name='tipo_herramienta',
            field=models.CharField(max_length=15, null=True),
        ),
    ]