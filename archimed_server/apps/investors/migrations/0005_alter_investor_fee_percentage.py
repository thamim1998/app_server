# Generated by Django 3.2.25 on 2024-11-14 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0004_alter_investor_fee_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor',
            name='fee_percentage',
            field=models.DecimalField(decimal_places=3, default=10.0, max_digits=5),
        ),
    ]
