# Generated by Django 3.0.6 on 2020-06-03 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creative_shop', '0006_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo_filename',
            field=models.ImageField(blank=True, upload_to='product_images'),
        ),
    ]
