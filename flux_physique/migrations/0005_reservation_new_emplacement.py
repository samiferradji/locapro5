# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0006_auto_20161113_1447'),
        ('flux_physique', '0004_historiquedutravail'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='new_emplacement',
            field=models.ForeignKey(to='refereces.Emplacement', default=1),
        ),
    ]
