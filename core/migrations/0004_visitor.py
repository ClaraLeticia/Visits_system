# Generated by Django 5.1.6 on 2025-02-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('cpf', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('rg', models.CharField(max_length=9, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
    ]
