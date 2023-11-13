# Generated by Django 4.1 on 2023-03-02 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customuser_is_subscribed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pos',
            old_name='name',
            new_name='pos_name',
        ),
        migrations.RemoveField(
            model_name='pos',
            name='description',
        ),
        migrations.RemoveField(
            model_name='pos',
            name='staff',
        ),
        migrations.AddField(
            model_name='customuser',
            name='pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.pos'),
        ),
    ]
