# Generated by Django 2.2.1 on 2020-10-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
    ]