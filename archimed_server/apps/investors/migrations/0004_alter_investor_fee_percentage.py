# Generated by Django 3.2.25 on 2024-11-14 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0003_investor_invested_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor',
            name='fee_percentage',
            field=models.DecimalField(decimal_places=3, default=0.001, max_digits=12),
        ),
    ]
