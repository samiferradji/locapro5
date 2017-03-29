# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0019_auto_20170311_1236'),
        ('flux_physique', '0037_auto_20170316_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametres',
            name='emplacement_expedition_transfert_entre_filiale',
            field=models.ForeignKey(to='refereces.Emplacement', verbose_name='Emplacement de reception des Transferts entre Filiales', related_name='emplacement_expedition_transfert_entre_filiale', default=1),
            preserve_default=False,
        ),
    ]
