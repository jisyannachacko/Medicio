# Generated by Django 5.2 on 2025-04-17 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
