# Generated by Django 3.1 on 2020-08-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='title',
            field=models.CharField(max_length=180, verbose_name='Title'),
        ),
    ]