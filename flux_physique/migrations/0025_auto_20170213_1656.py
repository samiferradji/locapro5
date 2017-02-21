# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0024_auto_20170213_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametres',
            name='process_vente_colis_complet',
            field=models.ForeignKey(related_name='vente_colis', to='refereces.TypesMouvementStock', verbose_name='Processus vente colis complets'),
        ),
    ]
