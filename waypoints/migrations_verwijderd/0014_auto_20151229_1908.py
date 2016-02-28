# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0013_auto_20151229_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peilbuisgegevens',
            name='borehole_id',
        ),
        migrations.DeleteModel(
            name='Peilbuisgegevens',
        ),
    ]
