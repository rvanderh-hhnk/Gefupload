# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0013_auto_20151229_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='waypoint',
            old_name='projectid',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='sondering',
            old_name='einddiepte_type',
            new_name='type_einddiepte',
        ),
        migrations.RemoveField(
            model_name='boring',
            name='bestand_boring',
        ),
        migrations.RemoveField(
            model_name='boring',
            name='gaf_id',
        ),
        migrations.RemoveField(
            model_name='boring',
            name='gdr_id',
        ),
        migrations.RemoveField(
            model_name='boring',
            name='gtlp_id',
        ),
        migrations.RemoveField(
            model_name='peilbuisgegevens',
            name='aantal_filters',
        ),
        migrations.RemoveField(
            model_name='peilbuisput',
            name='gtlp_id',
        ),
        migrations.RemoveField(
            model_name='peilbuisput',
            name='gtlpident',
        ),
        migrations.RemoveField(
            model_name='sondering',
            name='gaf_id',
        ),
        migrations.RemoveField(
            model_name='sondering',
            name='gdr_id',
        ),
        migrations.RemoveField(
            model_name='sondering',
            name='gtlp_id',
        ),
        migrations.AddField(
            model_name='boring',
            name='bestand_labproeven',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='boring',
            name='bestanden_corsa',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='boring',
            name='monstername',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='boring',
            name='project_naam',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='peilbuisgegevens',
            name='project_naam',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='peilbuisput',
            name='bestand_txt',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='peilbuisput',
            name='project_naam',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='projecten',
            name='project_id',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='sondering',
            name='bestanden_corsa',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='sondering',
            name='project_naam',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='sondering',
            name='sondeerklasse',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='waypoint',
            name='project_naam',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='peilbuisput',
            name='bestand_gef',
            field=models.CharField(unique=True, max_length=250),
        ),
    ]
