# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0019_auto_20170311_1236'),
        ('flux_physique', '0035_auto_20170315_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametres',
            name='process_expedition_transfert_entre_filiales',
            field=models.ForeignKey(to='refereces.TypesMouvementStock', related_name='expedition_transfert_entre_filiales', verbose_name='Processus extpédition des transferts entre filiales', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_reception_transfert_entre_filiales',
            field=models.ForeignKey(to='refereces.TypesMouvementStock', related_name='reception_transfert_entre_filiales', verbose_name='Processus réception des transferts entre filiales', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_transfert_entre_filiales',
            field=models.ForeignKey(to='refereces.TypesMouvementStock', related_name='transfert_entre_filiales', verbose_name='Processus transfert entre filiales', default=1),
            preserve_default=False,
        ),
    ]
