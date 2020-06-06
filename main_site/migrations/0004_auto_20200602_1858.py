# Generated by Django 3.0.6 on 2020-06-02 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0003_auto_20200601_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=2048),
        ),
        migrations.AlterField(
            model_name='user',
            name='forum_nickname',
            field=models.CharField(default='user_4439107', max_length=75),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
