# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0007_remove_peilbuisput_boring_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='peilbuisput',
            name='boring_id',
            field=models.ForeignKey(to='waypoints.Boring'),
            preserve_default=False,
        ),
    ]
