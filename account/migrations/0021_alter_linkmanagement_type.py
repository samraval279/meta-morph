# Generated by Django 3.2 on 2022-07-05 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20220705_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmanagement',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='links', to='account.linktype', verbose_name='type'),
        ),
    ]
