# Generated by Django 4.2.2 on 2023-06-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_rename_date_transaction_transaction_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(default=''),
        ),
    ]