# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0041_auto_20170317_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailsexpeditiontransfertsentrefiliale',
            name='nombre_colis',
        ),
        migrations.RemoveField(
            model_name='detailsexpeditiontransfertsentrefiliale',
            name='nombre_colis_frigo',
        ),
    ]
