# Generated by Django 3.2.5 on 2021-08-03 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20210803_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripimage',
            name='image',
            field=models.ImageField(upload_to='trip_images'),
        ),
    ]