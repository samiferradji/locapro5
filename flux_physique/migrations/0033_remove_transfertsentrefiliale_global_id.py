# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0032_auto_20170314_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfertsentrefiliale',
            name='global_id',
        ),
    ]
