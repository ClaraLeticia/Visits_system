# Generated by Django 5.1.6 on 2025-02-14 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_visits_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visits',
            options={'permissions': [('change_confirm_visits_employee', 'employee can change the status of visits')]},
        ),
    ]
