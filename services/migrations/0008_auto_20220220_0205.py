# Generated by Django 3.0.2 on 2022-02-20 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20220220_0142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='pricing',
            new_name='services_type',
        ),
    ]
