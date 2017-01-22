# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0011_auto_20170101_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='poids_colis',
            field=models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, verbose_name='Poids colis'),
        ),
    ]
