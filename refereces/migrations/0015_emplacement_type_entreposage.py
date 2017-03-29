# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0014_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='emplacement',
            name='type_entreposage',
            field=models.ForeignKey(to='refereces.TypeEntreposage', default=1, verbose_name="Type d'entreposage"),
        ),
    ]
