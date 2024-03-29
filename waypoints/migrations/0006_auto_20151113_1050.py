# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waypoints', '0005_auto_20151113_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('boring_id', models.IntegerField(null=True)),
                ('boringident', models.CharField(max_length=50, null=True)),
                ('x_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('y_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('mv_nap', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('dwarspositie', models.CharField(max_length=20, null=True)),
                ('datum_boring', models.DateTimeField(null=True)),
                ('bedrijf', models.CharField(max_length=50, null=True)),
                ('project_id', models.CharField(max_length=150, null=True)),
                ('type_boring', models.CharField(max_length=20, null=True)),
                ('methode_boring', models.CharField(max_length=20, null=True)),
                ('einddiepte', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('bestand_boring', models.CharField(max_length=50, null=True)),
                ('gtlp_id', models.IntegerField(null=True)),
                ('gdr_id', models.IntegerField(null=True)),
                ('gaf_id', models.IntegerField(null=True)),
                ('bestand_pdf', models.CharField(max_length=250, null=True)),
                ('bestand_gef', models.CharField(max_length=150, unique=True, null=True)),
                ('bestand_grondonderzoek', models.CharField(max_length=250, null=True)),
                ('gef_file', models.FileField(null=True, upload_to=b'')),
                ('gef_file_bf', models.BinaryField(null=True)),
                ('status', models.CharField(default=b'nee', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Filtergegevens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_id', models.IntegerField(null=True)),
                ('filterident', models.CharField(max_length=50, null=True)),
                ('bovenkant_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('onderkant_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_filter', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('status', models.CharField(default=b'nee', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Peilbuis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peilbuis_id', models.IntegerField(null=True)),
                ('peilbuisident', models.CharField(max_length=50, null=True)),
                ('bovenkant_peilbuis', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_peilbuis', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('lengte_zandvang', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('aantal_filters', models.IntegerField(null=True)),
                ('status', models.CharField(default=b'nee', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Peilbuisput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('borehole_id', models.IntegerField(null=True)),
                ('boreholeident', models.CharField(max_length=50, null=True)),
                ('boring_id', models.CharField(max_length=20, null=True)),
                ('peilbuisraai_id', models.CharField(max_length=20, null=True)),
                ('x_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('y_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('mv_nap', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('dwarspositie', models.CharField(max_length=20, null=True)),
                ('datum_plaatsing', models.DateTimeField(null=True)),
                ('aanwezig', models.CharField(max_length=20, null=True)),
                ('datum_verwijdering', models.DateTimeField(null=True)),
                ('bedrijf', models.CharField(max_length=50, null=True)),
                ('project_id', models.CharField(max_length=150, null=True)),
                ('type_peilbuisput', models.CharField(max_length=20, null=True)),
                ('aantal_peilbuizen', models.IntegerField(null=True)),
                ('bestand_peilbuisput', models.CharField(max_length=50, null=True)),
                ('bestand_parent', models.CharField(max_length=50, null=True)),
                ('gtlp_id', models.IntegerField(null=True)),
                ('bestand_gef', models.CharField(unique=True, max_length=150)),
                ('bestand_grondonderzoek', models.CharField(max_length=250, null=True)),
                ('gef_file', models.FileField(null=True, upload_to=b'')),
                ('status', models.CharField(default=b'nee', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Projecten',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(unique=True, max_length=150)),
                ('startdatum', models.DateTimeField(null=True)),
                ('project_status', models.CharField(default=b'in bewerking', max_length=32)),
                ('opmerking', models.CharField(max_length=150, null=True)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sondering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sondering_id', models.IntegerField(null=True)),
                ('sonderingident', models.CharField(max_length=50, null=True)),
                ('x_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('y_rd', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('mv_nap', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('dwarspositie', models.CharField(max_length=20, null=True)),
                ('datum_sondering', models.DateTimeField(null=True)),
                ('bedrijf', models.CharField(max_length=50, null=True)),
                ('project_id', models.CharField(max_length=150, null=True)),
                ('type_sondeeronderzoek', models.CharField(max_length=20, null=True)),
                ('methode_sondering', models.CharField(max_length=100, null=True)),
                ('einddiepte', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
                ('einddiepte_type', models.CharField(max_length=20, null=True)),
                ('bestand_sondering', models.CharField(max_length=50, null=True)),
                ('gtlp_id', models.IntegerField(null=True)),
                ('gdr_id', models.IntegerField(null=True)),
                ('gaf_id', models.IntegerField(null=True)),
                ('bestand_pdf', models.CharField(max_length=250, null=True)),
                ('bestand_gef', models.CharField(unique=True, max_length=150)),
                ('bestand_grondonderzoek', models.CharField(max_length=250, null=True)),
                ('voorboring_aanwezig', models.CharField(max_length=20, null=True)),
                ('gef_file', models.FileField(null=True, upload_to=b'')),
                ('status', models.CharField(default=b'nee', max_length=32)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('DateMutated', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='peilbuis',
            name='borehole_id',
            field=models.ForeignKey(to='waypoints.Peilbuisput'),
        ),
        migrations.AddField(
            model_name='filtergegevens',
            name='peilbuis_id',
            field=models.ForeignKey(to='waypoints.Peilbuis'),
        ),
    ]
