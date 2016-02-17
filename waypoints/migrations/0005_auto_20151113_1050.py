# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0004_auto_20151113_1043'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Boring',
        ),
        migrations.RemoveField(
            model_name='filtergegevens',
            name='peilbuis_id',
        ),
        migrations.RemoveField(
            model_name='peilbuis',
            name='borehole_id',
        ),
        migrations.RemoveField(
            model_name='projecten',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Sondering',
        ),
        migrations.DeleteModel(
            name='Filtergegevens',
        ),
        migrations.DeleteModel(
            name='Peilbuis',
        ),
        migrations.DeleteModel(
            name='Peilbuisput',
        ),
        migrations.DeleteModel(
            name='Projecten',
        ),
    ]
