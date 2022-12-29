# Generated by Django 4.1 on 2022-12-29 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('quantity_available', models.IntegerField(default=0)),
                ('reorder_level', models.IntegerField(blank=True, default=0)),
                ('status', models.CharField(blank=True, choices=[('Available', 'Item is currently available'), ('Restocking', 'Currently out of stock')], default='Available', max_length=20, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('quantity_restocked', models.IntegerField(blank=True, default=0, null=True)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('store', models.IntegerField(default=0)),
                ('sold', models.IntegerField(blank=True, default=0, null=True)),
                ('variance', models.IntegerField(default=0)),
                ('last_updated', models.DateField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'inventories',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_profit', models.FloatField(blank=True, default=0, null=True)),
                ('final_total_price', models.FloatField(blank=True, default=0, null=True)),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('method', models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Transfer', 'Transfer'), ('POS', 'POS')], default='Cash', max_length=50, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.pos')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(blank=True, max_length=250, null=True)),
                ('supplier_number', models.CharField(blank=True, max_length=100, null=True)),
                ('supplies', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(default=0)),
                ('cost_total', models.FloatField(default=0)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ims.inventory')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ims.sale')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('brand', models.CharField(blank=True, max_length=150, null=True)),
                ('product_code', models.CharField(max_length=100)),
                ('batch_no', models.CharField(blank=True, max_length=20, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('profit', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ims.category')),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='ims.product'),
        ),
        migrations.CreateModel(
            name='HistoricalSalesItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('total', models.FloatField(default=0)),
                ('cost_total', models.FloatField(default=0)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('last_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('inventory', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ims.inventory')),
                ('sale', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ims.sale')),
            ],
            options={
                'verbose_name': 'historical sales item',
                'verbose_name_plural': 'historical sales items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSale',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('total_profit', models.FloatField(blank=True, default=0, null=True)),
                ('final_total_price', models.FloatField(blank=True, default=0, null=True)),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(blank=True, editable=False, null=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('method', models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Transfer', 'Transfer'), ('POS', 'POS')], default='Cash', max_length=50, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='account.pos')),
            ],
            options={
                'verbose_name': 'historical sale',
                'verbose_name_plural': 'historical sales',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInventory',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('quantity_available', models.IntegerField(default=0)),
                ('reorder_level', models.IntegerField(blank=True, default=0)),
                ('status', models.CharField(blank=True, choices=[('Available', 'Item is currently available'), ('Restocking', 'Currently out of stock')], default='Available', max_length=20, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('quantity_restocked', models.IntegerField(blank=True, default=0, null=True)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('store', models.IntegerField(default=0)),
                ('sold', models.IntegerField(blank=True, default=0, null=True)),
                ('variance', models.IntegerField(default=0)),
                ('last_updated', models.DateField(blank=True, editable=False)),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ims.product')),
            ],
            options={
                'verbose_name': 'historical inventory',
                'verbose_name_plural': 'historical inventories',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ErrorTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_area', models.CharField(blank=True, max_length=250, null=True)),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Seen', 'Seen')], default='Pending', max_length=50, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
