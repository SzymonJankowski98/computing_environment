# Generated by Django 4.0 on 2021-12-25 11:05

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('computing_environment', '0007_alter_job_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='state',
            field=django_fsm.FSMField(default='available', max_length=50, protected=True),
        ),
    ]
