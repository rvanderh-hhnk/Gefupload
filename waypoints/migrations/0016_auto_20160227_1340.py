# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0015_projecten_aantal_peilbuizen'),
    ]

    operations = [
        migrations.AddField(
            model_name='boring',
            name='startdatum',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='peilbuisgegevens',
            name='startdatum',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='peilbuisput',
            name='startdatum',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='sondering',
            name='startdatum',
            field=models.DateTimeField(null=True),
        ),
    ]
