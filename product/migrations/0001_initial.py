# Generated by Django 2.2.5 on 2020-08-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=164, unique=True)),
                ('gold_wt', models.FloatField()),
                ('diamond_wt', models.FloatField()),
                ('price', models.FloatField()),
                ('product_type', models.CharField(choices=[('necklace', 'Necklace'), ('earrings', 'Earrings'), ('bangle', 'Bangle'), ('bracelet', 'Bracelet')], max_length=164)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=3)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True, max_length=300)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]