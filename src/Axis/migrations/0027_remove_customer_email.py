# Generated by Django 3.1.5 on 2021-01-09 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Axis', '0026_auto_20210109_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
    ]
