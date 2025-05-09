# Generated by Django 5.1.7 on 2025-04-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('delivered', 'Delivered'), ('processing', 'Processing'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
