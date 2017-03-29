# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0018_auto_20170310_1643'),
        ('flux_physique', '0025_auto_20170213_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailsTransfertEntreFiliale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('prix_achat', models.DecimalField(verbose_name='Achat HT', max_digits=9, decimal_places=2)),
                ('prix_vente', models.DecimalField(verbose_name='Vente HT', max_digits=9, decimal_places=2)),
                ('taux_tva', models.IntegerField(verbose_name='TVA')),
                ('shp', models.DecimalField(verbose_name='SHP', max_digits=9, decimal_places=2)),
                ('ppa_ht', models.DecimalField(verbose_name='PPA', max_digits=9, decimal_places=2)),
                ('n_lot', models.CharField(verbose_name='Lot', max_length=20)),
                ('date_peremption', models.DateField(verbose_name='DDP')),
                ('colisage', models.IntegerField(verbose_name='Colisage')),
                ('poids_boite', models.DecimalField(verbose_name='Poids boite', max_digits=9, decimal_places=2)),
                ('volume_boite', models.DecimalField(verbose_name='Volume boite', max_digits=9, decimal_places=2)),
                ('poids_colis', models.DecimalField(verbose_name='Poids du Colis', max_digits=9, decimal_places=2)),
                ('qtt', models.IntegerField(verbose_name='Quantité')),
                ('conformite', models.ForeignKey(to='refereces.StatutProduit', verbose_name='Statut', on_delete=django.db.models.deletion.PROTECT)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransfertsEntreFiliale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('original_id', models.PositiveIntegerField(verbose_name='transfert original')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('depuis_filiale', models.ForeignKey(related_name='depui_filiale', to='refereces.Filiale', verbose_name='Depuis filiale', on_delete=django.db.models.deletion.PROTECT)),
                ('statut_doc', models.ForeignKey(to='refereces.StatutDocument', verbose_name='Statut du transfert', on_delete=django.db.models.deletion.PROTECT)),
                ('vers_filiale', models.ForeignKey(to='refereces.Filiale', verbose_name='Vers filiale', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='parametres',
            name='exercice',
        ),
        migrations.AddField(
            model_name='parametres',
            name='filiale',
            field=models.ForeignKey(default=1, to='refereces.Filiale', verbose_name='Filiale'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailstransfertentrefiliale',
            name='entete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flux_physique.TransfertsEntreFiliale'),
        ),
        migrations.AddField(
            model_name='detailstransfertentrefiliale',
            name='produit',
            field=models.ForeignKey(to='refereces.Produit', verbose_name='Produit', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
