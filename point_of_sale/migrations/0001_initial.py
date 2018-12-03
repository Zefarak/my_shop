# Generated by Django 2.0.5 on 2018-12-02 13:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GiftRetailItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RetailOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Friendly ID')),
                ('title', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('date_expired', models.DateField(default=datetime.datetime(2018, 12, 2, 13, 11, 48, 664709, tzinfo=utc))),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('taxes', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('paid_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('printed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('1', 'New Order'), ('2', 'In Progress'), ('3', 'Ready for Send'), ('4', 'Sent'), ('5', 'Return'), ('6', 'Cancel'), ('7', 'Receipted'), ('8', 'Done')], default='1', max_length=1)),
                ('order_type', models.CharField(choices=[('r', 'Retail Order'), ('e', 'Eshop Invoice'), ('b', 'Return Order'), ('c', 'Cancel Order'), ('wa', 'Παραστατικό Εισαγωγής'), ('wr', 'Export Invoice')], default='r', max_length=1)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Συνολικό Κόστος Παραγγελίας')),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('payment_cost', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('day_sent', models.DateTimeField(blank=True, null=True)),
                ('eshop_order_id', models.CharField(blank=True, max_length=10, null=True)),
                ('eshop_session_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': '1. Παραστατικά Πωλήσεων',
                'ordering': ['-timestamp'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='RetailOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('qty', models.PositiveIntegerField(default=1)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('discount_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('is_find', models.BooleanField(default=False)),
                ('is_return', models.BooleanField(default=False)),
                ('total_value', models.DecimalField(decimal_places=0, default=0, help_text='qty*final_value', max_digits=20)),
                ('total_cost_value', models.DecimalField(decimal_places=0, default=0, help_text='qty*cost', max_digits=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='point_of_sale.RetailOrder')),
            ],
            options={
                'verbose_name_plural': '2. Προϊόντα Πωληθέντα',
                'ordering': ['-order__timestamp'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
    ]
