# Generated by Django 5.2 on 2025-04-24 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0013_blood_donor_register_registered_by_blood_users_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood_donor_register',
            name='registered_by',
        ),
        migrations.RemoveField(
            model_name='blood_users',
            name='user',
        ),
    ]
