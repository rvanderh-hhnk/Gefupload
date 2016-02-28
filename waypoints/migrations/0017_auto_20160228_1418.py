# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0016_auto_20160227_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecten',
            name='project_id',
            field=models.CharField(default=123, unique=True, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projecten',
            name='project_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
