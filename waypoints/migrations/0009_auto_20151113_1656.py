# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0008_peilbuisput_boring_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='boring',
            name='download_gef',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='peilbuisput',
            name='download_gef',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='sondering',
            name='download_gef',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='waypoint',
            name='download_gef',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='boring',
            name='bestand_gef',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
