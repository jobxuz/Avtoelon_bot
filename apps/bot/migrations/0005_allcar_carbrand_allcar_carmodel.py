# Generated by Django 5.1.3 on 2024-12-18 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_allcar_data_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='allcar',
            name='carbrand',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='allcar',
            name='carmodel',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
