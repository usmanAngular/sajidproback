# Generated by Django 3.0.2 on 2022-02-20 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20220220_0205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='services_type',
            new_name='pricing',
        ),
    ]
