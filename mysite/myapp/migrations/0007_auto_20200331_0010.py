# Generated by Django 3.0.3 on 2020-03-31 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200331_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curtourney',
            name='league',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.League'),
        ),
    ]
