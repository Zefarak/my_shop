# Generated by Django 2.0 on 2018-10-04 12:22

from django.db import migrations, models
import django.db.models.manager
import frontend.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('id_session', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('coupon_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[frontend.models.validate_positive_decimal])),
            ],
            options={
                'ordering': ['-id'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CartGiftItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[frontend.models.validate_positive_decimal])),
                ('price_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[frontend.models.validate_positive_decimal])),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[frontend.models.validate_positive_decimal])),
            ],
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CartRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_value', models.PositiveIntegerField(default=0)),
                ('shipping_value', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=50, null=True, unique=True)),
                ('date_created', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('cart_total_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_percent', models.PositiveIntegerField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='frontend.CategorySite')),
            ],
            options={
                'verbose_name_plural': 'Coupons',
                'ordering': ['active'],
            },
        ),
    ]
