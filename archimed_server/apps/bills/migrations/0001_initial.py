# Generated by Django 3.2.25 on 2024-11-13 23:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('investors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(choices=[('membership', 'Membership'), ('upfront_fees', 'Upfront Fees'), ('yearly_fees', 'Yearly Fees')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('due_date', models.DateField()),
                ('issue_date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='investors.investor')),
            ],
        ),
    ]
