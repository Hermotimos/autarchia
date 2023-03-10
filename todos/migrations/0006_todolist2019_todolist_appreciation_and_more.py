# Generated by Django 4.1.7 on 2023-03-09 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0005_todolist2020_todolist_eat1hbeforego_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TODOList2019',
            fields=[
            ],
            options={
                'verbose_name': 'TODO 2019',
                'verbose_name_plural': 'TODOs 2019',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('todos.todolist',),
        ),
        migrations.AddField(
            model_name='todolist',
            name='Appreciation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todolist',
            name='Helpfulness',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todolist',
            name='MILAM',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todolist',
            name='Mealx4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todolist',
            name='Mirroring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todolist',
            name='SATYR',
            field=models.BooleanField(default=False),
        ),
    ]