# Generated by Django 3.2 on 2022-07-04 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20220704_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='title',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='title'),
        ),
    ]
