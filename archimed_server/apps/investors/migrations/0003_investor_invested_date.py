# Generated by Django 3.2.25 on 2024-11-14 17:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0002_auto_20241114_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='invested_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
