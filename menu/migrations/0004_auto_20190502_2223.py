# Generated by Django 2.2 on 2019-05-03 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20190501_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['expiration_date']},
        ),
    ]
