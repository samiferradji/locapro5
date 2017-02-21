# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0022_auto_20170206_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achatsfournisseur',
            name='curr_exercice',
            field=models.IntegerField(verbose_name='Exrcice en cours', default=2017),
        ),
        migrations.AlterField(
            model_name='commandesclient',
            name='curr_exercice',
            field=models.IntegerField(verbose_name='Exrcice en cours', default=2017),
        ),
        migrations.AlterField(
            model_name='facturesclient',
            name='curr_exercice',
            field=models.IntegerField(verbose_name='Exrcice en cours', default=2017),
        ),
    ]
