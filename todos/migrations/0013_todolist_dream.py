# Generated by Django 4.1.7 on 2023-03-11 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0012_remove_todolist_contempl'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='DREAM',
            field=models.BooleanField(default=False),
        ),
    ]
