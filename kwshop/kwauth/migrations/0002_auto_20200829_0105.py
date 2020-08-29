# Generated by Django 2.2 on 2020-08-28 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kwauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kwuser',
            name='age',
            field=models.PositiveIntegerField(null=True, verbose_name='возраст'),
        ),
        migrations.AddField(
            model_name='kwuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users_ava'),
        ),
    ]
