# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0014_auto_20160225_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecten',
            name='aantal_peilbuizen',
            field=models.IntegerField(null=True),
        ),
    ]
