# Generated by Django 4.1.1 on 2022-10-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0009_inventory_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]