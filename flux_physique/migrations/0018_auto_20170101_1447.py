# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0017_auto_20161229_2210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achatsfournisseur',
            options={'permissions': (('valider_achats', 'Peut valider les achats'), ('voir_historique_achats', "Peut voir l'historique des achats"), ('importer_achats', 'Peut importer les achats'))},
        ),
        migrations.AlterField(
            model_name='achatsfournisseur',
            name='curr_exercice',
            field=models.IntegerField(default=2017, verbose_name='Exrcice en cours'),
        ),
        migrations.AlterField(
            model_name='commandesclient',
            name='curr_exercice',
            field=models.IntegerField(default=2017, verbose_name='Exrcice en cours'),
        ),
        migrations.AlterField(
            model_name='facturesclient',
            name='curr_exercice',
            field=models.IntegerField(default=2017, verbose_name='Exrcice en cours'),
        ),
    ]
