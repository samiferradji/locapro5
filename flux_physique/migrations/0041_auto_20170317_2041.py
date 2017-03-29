# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0019_auto_20170311_1236'),
        ('flux_physique', '0040_auto_20170316_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailsExpeditionTransfertsEntreFiliale',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(primary_key=True, serialize=False, editable=False, max_length=20)),
                ('nombre_colis', models.PositiveSmallIntegerField(verbose_name='Nombre de colis T° ambiante')),
                ('nombre_colis_frigo', models.PositiveSmallIntegerField(verbose_name='Nombre de colis T° 2 à 8°C')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpeditionTransfertsEntreFiliale',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(primary_key=True, serialize=False, editable=False, max_length=20)),
                ('livreur', models.CharField(verbose_name='Livreur ou démarcheur', max_length=50)),
                ('fourgon', models.CharField(verbose_name='Immatriculation du véhicule', max_length=15)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('statut_doc', models.ForeignKey(verbose_name='Statut du transfert', to='refereces.StatutDocument', on_delete=django.db.models.deletion.PROTECT)),
                ('vers_filiale', models.ForeignKey(verbose_name='Vers filiale', to='refereces.Filiale', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='transfertsentrefiliale',
            name='nombre_colis',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° ambiante'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transfertsentrefiliale',
            name='nombre_colis_frigo',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Nombre de colis T° 2 à 8°C'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailsexpeditiontransfertsentrefiliale',
            name='entete',
            field=models.ForeignKey(verbose_name='Entete', to='flux_physique.ExpeditionTransfertsEntreFiliale', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='detailsexpeditiontransfertsentrefiliale',
            name='transfert',
            field=models.ForeignKey(to='flux_physique.TransfertsEntreFiliale', verbose_name='N° du transfert'),
        ),
    ]
