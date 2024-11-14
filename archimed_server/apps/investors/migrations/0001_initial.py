# Generated by Django 3.2.25 on 2024-11-13 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('iban', models.CharField(max_length=34, unique=True)),
                ('invested_amount', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]