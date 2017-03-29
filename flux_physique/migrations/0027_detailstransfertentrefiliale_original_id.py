# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0026_auto_20170310_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailstransfertentrefiliale',
            name='original_id',
            field=models.PositiveIntegerField(verbose_name='transfert original', default=2000),
            preserve_default=False,
        ),
    ]
