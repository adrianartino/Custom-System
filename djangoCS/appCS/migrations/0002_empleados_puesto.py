# Generated by Django 3.2.5 on 2021-07-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados',
            name='puesto',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
