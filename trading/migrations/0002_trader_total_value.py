# Generated by Django 5.0.6 on 2024-07-04 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trader',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10),
        ),
    ]
