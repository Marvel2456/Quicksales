# Generated by Django 4.1.1 on 2022-10-13 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0006_alter_category_category_name_alter_inventory_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesitem',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]