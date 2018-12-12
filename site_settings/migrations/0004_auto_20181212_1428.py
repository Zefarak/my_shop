# Generated by Django 2.0 on 2018-12-12 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0003_auto_20181204_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorders',
            name='date_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία'),
        ),
        migrations.AlterField(
            model_name='paymentorders',
            name='final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Τελική Αξίσ'),
        ),
        migrations.AlterField(
            model_name='paymentorders',
            name='paid_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Πληρωτέο Ποσό'),
        ),
        migrations.AlterField(
            model_name='paymentorders',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Φόροι'),
        ),
        migrations.AlterField(
            model_name='paymentorders',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Αξία'),
        ),
    ]
