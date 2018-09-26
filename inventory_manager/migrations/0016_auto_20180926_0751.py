# Generated by Django 2.0.5 on 2018-09-26 04:51

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('inventory_manager', '0015_auto_20180926_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitemattribute',
            name='size_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Size'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.datetime(2018, 9, 26, 4, 51, 19, 889597, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='orderitemattribute',
            unique_together={('order_item_related', 'size_related')},
        ),
    ]
