# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0010_auto_20161224_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='adresse',
            field=models.CharField(null=True, blank=True, verbose_name='Adresse de livraion', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='axe',
            field=models.ForeignKey(verbose_name='Axe de livaion', blank=True, to='refereces.Axe', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='client',
            name='commune',
            field=models.ForeignKey(verbose_name='Commune', blank=True, to='refereces.Commune', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='client',
            name='telephone',
            field=models.CharField(null=True, blank=True, verbose_name='Téléphone', max_length=30),
        ),
        migrations.AlterField(
            model_name='commune',
            name='code_commune',
            field=models.PositiveSmallIntegerField(null=True, unique=True, blank=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='wilaya',
            field=models.ForeignKey(verbose_name='Wilaya', blank=True, to='refereces.Wilaya', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
