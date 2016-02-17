# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0013_auto_20151229_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='peilbuisgegevens',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
        ),
        migrations.AddField(
            model_name='peilbuisgegevens',
            name='project_id',
            field=models.CharField(max_length=150, null=True),
        ),
        
    ]
