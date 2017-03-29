# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0033_remove_transfertsentrefiliale_global_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailstransfertentrefiliale',
            name='id',
            field=models.CharField(serialize=False, editable=False, max_length=20, primary_key=True),
        ),
    ]
