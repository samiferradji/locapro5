# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='globaltransfertsentrefiliale',
            name='original_id',
        ),
        migrations.AlterField(
            model_name='globaldetailstransfertentrefiliale',
            name='id',
            field=models.CharField(serialize=False, max_length=20, primary_key=True),
        ),
        migrations.AlterField(
            model_name='globaltransfertsentrefiliale',
            name='id',
            field=models.CharField(serialize=False, max_length=20, primary_key=True),
        ),
    ]
