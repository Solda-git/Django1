# Generated by Django 2.2 on 2020-08-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwauth', '0002_auto_20200829_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='kwuser',
            name='sex',
            field=models.CharField(blank=True, max_length=1, verbose_name='пол'),
        ),
    ]
