# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0014_auto_20160203_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boring',
            name='bestand_pdf',
            field=models.CharField(max_length=150, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='sondering',
            name='bestand_pdf',
            field=models.CharField(max_length=150, unique=True, null=True),
        ),
    ]
