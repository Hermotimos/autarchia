# Generated by Django 4.1.7 on 2023-03-11 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0013_todolist_dream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='DREAMS',
        ),
    ]
