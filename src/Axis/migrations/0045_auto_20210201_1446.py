# Generated by Django 3.1.5 on 2021-02-01 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Axis', '0044_auto_20210201_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorylayer5',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer4'),
        ),
        migrations.AlterField(
            model_name='categorylayer6',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer5'),
        ),
    ]
