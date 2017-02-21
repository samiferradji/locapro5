# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0013_auto_20170116_1508'),
        ('flux_physique', '0020_auto_20170116_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='validation',
            name='boites_en_vrac',
            field=models.IntegerField(default=0, verbose_name='Nombre de boites en VRAC'),
        ),
        migrations.AddField(
            model_name='validation',
            name='colis_count',
            field=models.IntegerField(default=0, verbose_name='Nombre de colis'),
        ),
        migrations.AddField(
            model_name='validation',
            name='colis_en_palette',
            field=models.IntegerField(default=0, verbose_name='Nombre de colis palettisés'),
        ),
        migrations.AddField(
            model_name='validation',
            name='motif_mvnt',
            field=models.ForeignKey(default=1, verbose_name='Motif du mouvement de stock', to='refereces.TypesMouvementStock'),
        ),
        migrations.AddField(
            model_name='validation',
            name='origin_created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='validation',
            name='origine_created_by',
            field=models.ForeignKey(default=2, related_name='user_creat_Bon', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='validation',
            name='boite_count',
            field=models.IntegerField(verbose_name='Nombre de boites'),
        ),
        migrations.AlterField(
            model_name='validation',
            name='ligne_count',
            field=models.IntegerField(verbose_name='Nombre de lignes'),
        ),
    ]
