# Generated by Django 3.0.2 on 2020-01-18 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_number',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
