# Generated by Django 4.2.2 on 2023-06-22 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0010_expensecategory_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products'),
        ),
    ]
