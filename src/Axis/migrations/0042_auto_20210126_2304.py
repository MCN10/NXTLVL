# Generated by Django 3.1.5 on 2021-01-26 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Axis', '0041_auto_20210115_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryLayer2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('has_subcategory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category Layer 2',
            },
        ),
        migrations.CreateModel(
            name='CategoryLayer3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('has_subcategory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category Layer 3',
            },
        ),
        migrations.CreateModel(
            name='CategoryLayer4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('has_subcategory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category Layer 4',
            },
        ),
        migrations.CreateModel(
            name='CategoryLayer5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('has_subcategory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category Layer 5',
            },
        ),
        migrations.CreateModel(
            name='CategoryLayer6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('has_subcategory', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category Layer 6',
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='count',
        ),
        migrations.AddField(
            model_name='category',
            name='has_subcategory',
            field=models.BooleanField(default=False),
        ),
    ]