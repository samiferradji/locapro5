# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0019_auto_20170311_1236'),
        ('flux_physique', '0036_auto_20170316_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailstransfertentrefiliale',
            name='depuis_emplacement',
            field=models.ForeignKey(related_name='depuis_empl_G', on_delete=django.db.models.deletion.PROTECT, verbose_name='Depuis Empl', default=1, to='refereces.Emplacement'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailstransfertentrefiliale',
            name='vers_emplacement',
            field=models.ForeignKey(related_name='vers_empl_G', on_delete=django.db.models.deletion.PROTECT, verbose_name='Vers Empl', default=1, to='refereces.Emplacement'),
            preserve_default=False,
        ),
    ]
