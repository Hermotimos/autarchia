# Generated by Django 4.1.7 on 2023-03-03 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_todolist_greenveggies'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]