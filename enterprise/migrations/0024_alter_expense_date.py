# Generated by Django 4.2.2 on 2023-06-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0023_expense_e_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
