# Generated by Django 2.0 on 2018-03-28 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_auto_20180328_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of project', max_length=200)),
                ('projectID', models.IntegerField()),
            ],
        ),
    ]
