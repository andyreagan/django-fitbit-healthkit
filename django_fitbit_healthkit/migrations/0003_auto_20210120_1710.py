# Generated by Django 3.1.5 on 2021-01-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbit', '0002_auto_20210120_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitbituser',
            name='fitbit_id',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
