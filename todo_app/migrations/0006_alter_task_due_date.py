# Generated by Django 3.2.25 on 2024-09-16 22:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0005_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
