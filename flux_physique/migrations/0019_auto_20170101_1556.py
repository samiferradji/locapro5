# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0018_auto_20170101_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturesclient',
            name='date_commande',
        ),
        migrations.RemoveField(
            model_name='facturesclient',
            name='n_commande',
        ),
        migrations.AddField(
            model_name='facturesclient',
            name='date_commande_original',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date de la commande'),
        ),
        migrations.AddField(
            model_name='facturesclient',
            name='date_facture',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date facture'),
        ),
        migrations.AddField(
            model_name='facturesclient',
            name='n_commande_original',
            field=models.CharField(default=1, max_length=10, verbose_name='Numéro de la commande'),
        ),
        migrations.AddField(
            model_name='facturesclient',
            name='n_facrure',
            field=models.CharField(default=1, max_length=10, verbose_name='Numéro de facture'),
        ),
    ]
