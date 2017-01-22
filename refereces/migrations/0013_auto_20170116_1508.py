# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0012_produit_poids_colis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='poids',
            field=models.DecimalField(decimal_places=2, default=0, verbose_name='Poids', blank=True, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='poids_colis',
            field=models.DecimalField(decimal_places=2, default=0, verbose_name='Poids colis', blank=True, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='volume',
            field=models.DecimalField(decimal_places=2, default=0, verbose_name='Volume', blank=True, max_digits=10),
        ),
    ]
