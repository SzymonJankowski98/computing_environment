# Generated by Django 4.0 on 2022-01-18 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computing_environment', '0024_worker_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='ip_address',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
