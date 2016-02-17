# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0002_auto_20151113_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filtergegevens',
            name='peilbuis_id',
        ),
        migrations.RemoveField(
            model_name='peilbuis',
            name='borehole_id',
        ),
        migrations.AlterField(
            model_name='boring',
            name='boring_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='filtergegevens',
            name='filter_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='peilbuis',
            name='peilbuis_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='peilbuisput',
            name='borehole_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sondering',
            name='sondering_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='boring',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filtergegevens',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peilbuis',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peilbuisput',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sondering',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        
    ]
