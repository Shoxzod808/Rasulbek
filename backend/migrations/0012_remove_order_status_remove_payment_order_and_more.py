# Generated by Django 5.0.3 on 2024-04-29 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_orderproduct_options_refund_refundproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.AddField(
            model_name='payment',
            name='driver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='DriverForPayment', to='backend.driver'),
            preserve_default=False,
        ),
    ]
