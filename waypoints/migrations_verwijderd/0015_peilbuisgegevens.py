# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waypoints', '0014_auto_20151229_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Peilbuisgegevens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peilbuis_id', models.IntegerField(null=True)),
                ('peilbuisident', models.CharField(max_length=50, null=True)),
                ('bovenkant_peilbuis', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_peilbuis', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_zandvang', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('binnendiameter_mm', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('bovenkant_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('onderkant_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('aantal_filters', models.IntegerField(null=True)),
                ('bestand_meetreeks', models.CharField(max_length=250, null=True)),
                ('status', models.CharField(default=b'nog niet gecontroleerd', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('borehole_id', models.ForeignKey(to='waypoints.Peilbuisput')),
            ],
        ),
    ]
