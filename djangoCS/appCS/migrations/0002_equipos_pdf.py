# Generated by Django 3.2.5 on 2021-08-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='pdf',
            field=models.FileField(null=True, upload_to='pdfequipos'),
        ),
    ]
