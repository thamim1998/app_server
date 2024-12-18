# Generated by Django 3.2.25 on 2024-11-17 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0002_alter_investment_fee_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='investment_fees_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investment',
            name='years_paid',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
