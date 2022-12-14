# Generated by Django 4.1.1 on 2022-10-11 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0002_remove_product_cost_price_remove_product_sale_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ims.product', unique=True),
        ),
    ]
