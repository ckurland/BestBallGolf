# Generated by Django 3.0.3 on 2020-02-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200218_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='joinKey',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
