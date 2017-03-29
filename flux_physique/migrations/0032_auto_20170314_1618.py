# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0031_auto_20170312_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfertsentrefiliale',
            name='id',
            field=models.CharField(serialize=False, editable=False, max_length=20, primary_key=True),
        ),
    ]
