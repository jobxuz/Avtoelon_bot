# Generated by Django 5.1.3 on 2024-12-18 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_allcar_carbrand_allcar_carmodel'),
        ('user', '0003_detecsia_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='allcar',
            name='detecsia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.detecsia'),
        ),
    ]