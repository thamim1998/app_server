# Generated by Django 3.2.25 on 2024-11-16 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0006_auto_20241116_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investor',
            name='fee_percentage',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='invested_date',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='upfront_fees_paid',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='years_paid',
        ),
        migrations.AlterField(
            model_name='investor',
            name='invested_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
