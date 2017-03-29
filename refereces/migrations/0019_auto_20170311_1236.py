# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0018_auto_20170310_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typesmouvementstock',
            name='point_boite',
        ),
        migrations.RemoveField(
            model_name='typesmouvementstock',
            name='point_colis',
        ),
        migrations.RemoveField(
            model_name='typesmouvementstock',
            name='point_colis_palettise',
        ),
        migrations.RemoveField(
            model_name='typesmouvementstock',
            name='point_ligne',
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_boite_execution',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par boites executée', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_boite_validation',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par boite validée', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis_execution',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par colis executé', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis_palettise_execution',
            field=models.SmallIntegerField(blank=True, verbose_name='Point par colis palettisés executée', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis_palettise_validation',
            field=models.SmallIntegerField(blank=True, verbose_name='Point par colis palettisé validé', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis_validation',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par colis validée', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_ligne_execution',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par ligne executée', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_ligne_saisie',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par ligne saisie', null=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_ligne_validation',
            field=models.SmallIntegerField(blank=True, verbose_name='Points par ligne validée', null=True),
        ),
    ]
