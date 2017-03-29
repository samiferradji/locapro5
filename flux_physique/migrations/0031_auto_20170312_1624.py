# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0030_auto_20170312_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfertsentrefiliale',
            name='global_id',
            field=models.CharField(editable=False, max_length=20, verbose_name='Identifiant groupe'),
        ),
    ]
