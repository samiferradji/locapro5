# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0034_auto_20170315_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='id_in_content_type',
            field=models.CharField(verbose_name='Original id', max_length=20),
        ),
    ]
