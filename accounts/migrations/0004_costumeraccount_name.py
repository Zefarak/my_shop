# Generated by Django 2.0 on 2018-09-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180917_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='costumeraccount',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
