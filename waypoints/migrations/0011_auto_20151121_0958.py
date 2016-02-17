# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0010_auto_20151116_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecten',
            name='aantal_boringen',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='projecten',
            name='aantal_peilbuisputten',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='projecten',
            name='aantal_sonderingen',
            field=models.IntegerField(null=True),
        ),
    ]
