# Generated by Django 3.0.6 on 2020-06-01 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creative_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(default='Описание моего прекрастного магазина'),
        ),
        migrations.AddField(
            model_name='shop',
            name='name',
            field=models.CharField(default='Мой магазин', max_length=255),
        ),
    ]
