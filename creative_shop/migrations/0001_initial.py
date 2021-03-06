# Generated by Django 3.0.6 on 2020-06-01 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Метод доставки', max_length=255)),
                ('slug', models.CharField(default='method', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('free_until', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Название товара', max_length=255)),
                ('description', models.TextField(blank=True, default='Описание товара')),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='products', to='creative_shop.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='CardItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', related_query_name='items', to='creative_shop.Card')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='creative_shop.Product')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='cards', to='creative_shop.Shop'),
        ),
        migrations.AddField(
            model_name='card',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='creative_shop.CardStatus'),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_user', related_query_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ActiveDeliveryMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_until', models.DateTimeField(auto_now_add=True)),
                ('delivery_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_shop', to='creative_shop.DeliveryMethod')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='active_delivery_methods', to='creative_shop.Shop')),
            ],
        ),
    ]
