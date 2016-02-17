# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0003_auto_20151113_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='filtergegevens',
            name='peilbuis_id',
            field=models.ForeignKey(default=1, to='waypoints.Peilbuis'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peilbuis',
            name='borehole_id',
            field=models.ForeignKey(default=1, to='waypoints.Peilbuisput'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='DateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
