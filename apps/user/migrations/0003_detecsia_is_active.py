# Generated by Django 5.1.3 on 2024-12-13 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_detecsia'),
    ]

    operations = [
        migrations.AddField(
            model_name='detecsia',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]