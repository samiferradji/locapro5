# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_data', '0002_auto_20170311_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='globaltransfertsentrefiliale',
            name='nombre_colis',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° ambiante'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='globaltransfertsentrefiliale',
            name='nombre_colis_frigo',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° 2 à 8°C'),
            preserve_default=False,
        ),
    ]
