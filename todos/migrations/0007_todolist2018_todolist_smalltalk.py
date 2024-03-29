# Generated by Django 4.1.7 on 2023-03-09 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_todolist2019_todolist_appreciation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TODOList2018',
            fields=[
            ],
            options={
                'verbose_name': 'TODO 2018',
                'verbose_name_plural': 'TODOs 2018',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('todos.todolist',),
        ),
        migrations.AddField(
            model_name='todolist',
            name='SmallTalk',
            field=models.BooleanField(default=False),
        ),
    ]
