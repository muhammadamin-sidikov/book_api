# Generated by Django 5.2.4 on 2025-07-24 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
