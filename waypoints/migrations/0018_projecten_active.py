# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0017_auto_20160228_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecten',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
