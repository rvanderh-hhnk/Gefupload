# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0009_auto_20151113_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boring',
            name='bestand_gef',
            field=models.CharField(unique=True, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='name',
            field=models.CharField(unique=True, max_length=75),
            preserve_default=False,
        ),
    ]
