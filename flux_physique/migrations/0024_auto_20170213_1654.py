# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0016_magasin_type_entreposage'),
        ('flux_physique', '0023_auto_20170206_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametres',
            name='process_achat',
            field=models.ForeignKey(default=1, to='refereces.TypesMouvementStock', verbose_name='Processus achat', related_name='Achat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_entreposage',
            field=models.ForeignKey(default=1, to='refereces.TypesMouvementStock', verbose_name='Processus entreposage', related_name='entreposage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_etalage',
            field=models.ForeignKey(default=1, to='refereces.TypesMouvementStock', verbose_name='Processus etalage', related_name='etalage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_transfer',
            field=models.ForeignKey(default=1, to='refereces.TypesMouvementStock', verbose_name='Processus transfert interne', related_name='transfert_process'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametres',
            name='process_vente_colis_complet',
            field=models.ForeignKey(default=1, to='refereces.TypesMouvementStock', verbose_name='Processus vente complets', related_name='vente_colis'),
            preserve_default=False,
        ),
    ]
