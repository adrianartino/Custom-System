# Generated by Django 4.0.4 on 2022-05-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0022_requisicioncompraalmacen_fehca_requientrada'),
    ]

    operations = [
        migrations.AddField(
            model_name='herramientasalmacen',
            name='nombre_corto',
            field=models.CharField(max_length=60, null=True),
        ),
    ]