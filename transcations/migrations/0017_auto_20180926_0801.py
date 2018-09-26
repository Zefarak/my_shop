# Generated by Django 2.0.5 on 2018-09-26 05:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transcations', '0016_auto_20180926_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2018, 9, 26, 5, 1, 10, 564333, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='genericexpense',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2018, 9, 26, 5, 1, 10, 564333, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2018, 9, 26, 5, 1, 10, 564333, tzinfo=utc)),
        ),
    ]
