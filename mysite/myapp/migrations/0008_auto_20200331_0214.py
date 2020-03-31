# Generated by Django 3.0.3 on 2020-03-31 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20200331_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='activeDraft',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='league',
            name='endDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='league',
            name='tID',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='CurTourney',
        ),
    ]
