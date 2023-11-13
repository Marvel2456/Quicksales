# Generated by Django 4.1 on 2023-04-18 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_name_pos_pos_name_remove_pos_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_category', models.IntegerField(default=0)),
                ('max_staff', models.IntegerField(default=0)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.plan'),
        ),
    ]
