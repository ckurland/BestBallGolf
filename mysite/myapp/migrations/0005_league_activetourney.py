# Generated by Django 3.0.3 on 2020-03-31 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_curtourney_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='activeTourney',
            field=models.IntegerField(default=0),
        ),
    ]
