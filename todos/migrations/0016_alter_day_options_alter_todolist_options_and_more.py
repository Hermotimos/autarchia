# Generated by Django 4.1.7 on 2023-03-25 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0015_year_month_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['-daydate']},
        ),
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-date__daydate']},
        ),
        migrations.AlterModelOptions(
            name='todolist2023',
            options={'ordering': ['-date__daydate'], 'verbose_name': 'TODO 2023', 'verbose_name_plural': 'TODOs 2023'},
        ),
        migrations.RenameField(
            model_name='day',
            old_name='date',
            new_name='daydate',
        ),
    ]
