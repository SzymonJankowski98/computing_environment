# Generated by Django 3.2.9 on 2021-12-11 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computing_environment', '0002_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='sent',
            field=models.DateTimeField(null=True),
        ),
    ]
