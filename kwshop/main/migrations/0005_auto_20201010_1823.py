# Generated by Django 2.2.1 on 2020-10-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='productcat',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
