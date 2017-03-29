# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0038_parametres_emplacement_expedition_transfert_entre_filiale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validation',
            name='id_in_content_type',
            field=models.CharField(verbose_name='Id in content type', max_length=20),
        ),
    ]
