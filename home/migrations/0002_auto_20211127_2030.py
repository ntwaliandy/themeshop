# Generated by Django 3.1.6 on 2021-11-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='compatibility',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
