# Generated by Django 3.2 on 2022-06-21 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20220621_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subtitle',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='subtitle'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='video',
            name='upload_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL, verbose_name='upload by'),
        ),
    ]
