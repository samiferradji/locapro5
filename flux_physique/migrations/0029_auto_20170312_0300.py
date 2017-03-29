# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0028_auto_20170311_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motifsinventaire',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='motifsinventaire',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='motifsinventaire',
            name='modified_date',
        ),
    ]
