# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0021_auto_20170124_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achatsfournisseur',
            name='curr_exercice',
            field=models.IntegerField(default=2016, verbose_name='Exrcice en cours'),
        ),
        migrations.AlterField(
            model_name='commandesclient',
            name='curr_exercice',
            field=models.IntegerField(default=2016, verbose_name='Exrcice en cours'),
        ),
        migrations.AlterField(
            model_name='facturesclient',
            name='curr_exercice',
            field=models.IntegerField(default=2016, verbose_name='Exrcice en cours'),
        ),
    ]
