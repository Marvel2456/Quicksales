# Generated by Django 4.1 on 2022-11-30 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0009_errorticket_staus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errorticket',
            old_name='staus',
            new_name='status',
        ),
    ]