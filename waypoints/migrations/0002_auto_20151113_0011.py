# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waypoint',
            name='DateCreated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 13, 0, 11, 30, 567000)),
        ),
    ]
