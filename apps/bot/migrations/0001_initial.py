# Generated by Django 5.1.3 on 2024-12-11 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBotConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_token', models.CharField(default='token', max_length=255)),
                ('secret_key', models.CharField(default='secret_key', max_length=255)),
                ('webhook_url', models.URLField(default='https://api.telegram.org/', max_length=255)),
                ('admin', models.IntegerField(default=1235678)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
