# Generated by Django 3.2 on 2022-07-04 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20220630_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmanagement',
            name='type',
            field=models.CharField(choices=[('socialmedia', 'socialmedia'), ('videogame', 'videogame'), ('metaverse', 'metaverse')], max_length=30, null=True, verbose_name='type'),
        ),
    ]
