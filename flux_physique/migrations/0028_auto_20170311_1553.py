# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0027_detailstransfertentrefiliale_original_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailstransfertentrefiliale',
            name='original_id',
            field=models.PositiveIntegerField(verbose_name='detail transfert original'),
        ),
    ]
