# Generated by Django 5.0.3 on 2024-03-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='uuid',
            field=models.UUIDField(default=1),
        ),
    ]
