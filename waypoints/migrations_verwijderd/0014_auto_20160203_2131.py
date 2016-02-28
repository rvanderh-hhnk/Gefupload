# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0013_auto_20151229_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boring',
            name='bestand_pdf',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='sondering',
            name='bestand_pdf',
            field=models.FileField(null=True, upload_to=b''),
        ),
    ]
