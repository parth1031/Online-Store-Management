# Generated by Django 4.2.7 on 2023-11-06 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cart_cartitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
