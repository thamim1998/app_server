# Generated by Django 3.2.25 on 2024-11-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='due_date',
        ),
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
