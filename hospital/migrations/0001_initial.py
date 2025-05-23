# Generated by Django 5.2 on 2025-04-17 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blood_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Users', models.CharField(max_length=30)),
                ('Blood_Type', models.CharField(max_length=5)),
                ('Result', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Blood_Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hospital_Name', models.CharField(max_length=30)),
                ('District', models.CharField(default='district', max_length=30)),
                ('Blood_Type', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital_Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hospital_Name', models.CharField(max_length=30)),
                ('Address1', models.CharField(max_length=1024)),
                ('District', models.CharField(max_length=30)),
                ('PinCode', models.CharField(max_length=8)),
                ('PH_number', models.CharField(max_length=30)),
                ('E_mail', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=30)),
            ],
        ),
    ]
