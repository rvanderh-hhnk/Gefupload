# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0006_auto_20151113_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peilbuisput',
            name='boring_id',
        ),
    ]
