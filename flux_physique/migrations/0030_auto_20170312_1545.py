# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import flux_physique.models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0029_auto_20170312_0300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailstransfertentrefiliale',
            name='original_id',
        ),
        migrations.RemoveField(
            model_name='transfertsentrefiliale',
            name='original_id',
        ),
        migrations.AddField(
            model_name='transfertsentrefiliale',
            name='global_id',
            field=models.PositiveIntegerField(verbose_name='Identifiant groupe',
                                              ),
        ),
    ]
