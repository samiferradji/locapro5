# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0042_auto_20170318_0231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfertsentrefiliale',
            options={'permissions': (('ajouter_tef', 'Peut ajouter transferts entre filiale'), ('confirmer_tef', 'Peut confirmer transferts entre filiale'), ('expedier_tef', 'Peut expédier transferts entre filiale'), ('recevoir_tef', 'Peut recevoir transferts entre filiale'), ('voir_historique', "Peut voire l'historique des transferts entre filiale"))},
        ),
        migrations.AlterField(
            model_name='transfertsentrefiliale',
            name='nombre_colis',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° ambiante'),
        ),
        migrations.AlterField(
            model_name='transfertsentrefiliale',
            name='nombre_colis_frigo',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° 2 à 8°C'),
        ),
    ]
