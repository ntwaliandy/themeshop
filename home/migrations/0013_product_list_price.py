# Generated by Django 3.1.6 on 2021-12-13 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_product_exlusive'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='list_price',
            field=models.IntegerField(default=23),
            preserve_default=False,
        ),
    ]
