# Generated by Django 3.1.5 on 2021-02-01 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Axis', '0043_auto_20210126_2308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-date_added',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='categorylayer2',
            options={'ordering': ('-date_updated',), 'verbose_name': 'Category Layer 2'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='has_subcategory',
        ),
        migrations.RemoveField(
            model_name='categorylayer2',
            name='has_subcategory',
        ),
        migrations.RemoveField(
            model_name='categorylayer3',
            name='has_subcategory',
        ),
        migrations.RemoveField(
            model_name='categorylayer4',
            name='has_subcategory',
        ),
        migrations.RemoveField(
            model_name='categorylayer5',
            name='has_subcategory',
        ),
        migrations.RemoveField(
            model_name='categorylayer6',
            name='has_subcategory',
        ),
        migrations.AddField(
            model_name='category',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categorylayer2',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.category'),
        ),
        migrations.AddField(
            model_name='categorylayer2',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categorylayer3',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer2'),
        ),
        migrations.AddField(
            model_name='categorylayer3',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categorylayer4',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer3'),
        ),
        migrations.AddField(
            model_name='categorylayer4',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categorylayer5',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer5'),
        ),
        migrations.AddField(
            model_name='categorylayer5',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categorylayer6',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='souscatégories', to='Axis.categorylayer6'),
        ),
        migrations.AddField(
            model_name='categorylayer6',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
