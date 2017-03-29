# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0015_emplacement_type_entreposage'),
    ]

    operations = [
        migrations.AddField(
            model_name='magasin',
            name='type_entreposage',
            field=models.ForeignKey(default=1, to='refereces.TypeEntreposage', verbose_name="Type d'entreposage principal"),
        ),
    ]
