# Generated by Django 4.2.2 on 2023-06-27 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0019_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='paypal_address',
        ),
    ]