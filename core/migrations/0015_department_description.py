# Generated by Django 5.1.6 on 2025-02-14 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_visits_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
