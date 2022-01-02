# Generated by Django 4.0 on 2021-12-31 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computing_environment', '0012_alter_job_options_job_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='memory_usage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='processor_usage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
