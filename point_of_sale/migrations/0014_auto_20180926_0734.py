# Generated by Django 2.0.5 on 2018-09-26 04:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0013_auto_20180926_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailorder',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2018, 9, 26, 4, 33, 59, 792565, tzinfo=utc)),
        ),
    ]
