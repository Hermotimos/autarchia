# Generated by Django 4.1.7 on 2023-03-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='greenveggies',
            field=models.BooleanField(default=False),
        ),
    ]