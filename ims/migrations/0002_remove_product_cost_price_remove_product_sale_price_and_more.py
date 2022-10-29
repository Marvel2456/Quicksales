# Generated by Django 4.1.1 on 2022-10-01 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
        migrations.AddField(
            model_name='inventory',
            name='cost_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='sale_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]