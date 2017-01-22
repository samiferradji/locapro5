# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0019_auto_20170101_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsfacturesclient',
            name='ref_unique',
            field=models.CharField(default=0, max_length=20, verbose_name='reference_unique'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='poids_boite',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Poids boite'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='poids_colis',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Poids du Colis'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='volume_boite',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Volume boite'),
        ),
    ]
