# Generated by Django 4.2.2 on 2023-06-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0026_alter_expensecategory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='ec_code',
            field=models.CharField(default='b936ac63-90d6-496e-b290-52703a2aa5b7', max_length=50),
        ),
    ]
