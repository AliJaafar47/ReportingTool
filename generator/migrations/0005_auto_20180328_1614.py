# Generated by Django 2.0 on 2018-03-28 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0004_auto_20180328_1442'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Abbreviation',
            new_name='Short_Name',
        ),
    ]