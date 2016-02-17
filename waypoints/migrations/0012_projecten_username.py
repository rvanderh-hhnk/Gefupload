# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0011_auto_20151121_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecten',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
