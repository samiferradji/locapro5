# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalAxe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('axe', models.CharField(verbose_name='Axe de livraion', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('dossier', models.CharField(unique=True, verbose_name='Dossier Client', max_length=20)),
                ('nom_prenom', models.CharField(unique=True, verbose_name='Nom Complet du client', max_length=50)),
                ('adresse', models.CharField(null=True, verbose_name='Adresse de livraion', blank=True, max_length=100)),
                ('telephone', models.CharField(null=True, verbose_name='Téléphone', blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalCommune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code_commune', models.PositiveSmallIntegerField(unique=True, verbose_name='Code', blank=True, null=True)),
                ('commune', models.CharField(unique=True, verbose_name='Nom de la commune', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalDci',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code_dci', models.CharField(unique=True, verbose_name='Code DCI', max_length=30)),
                ('dci', models.CharField(verbose_name='DCI', max_length=50)),
                ('dosage', models.CharField(verbose_name='Dosage', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalDetailsTransfertEntreFiliale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlobalFiliale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('filiale', models.CharField(verbose_name='Nom de la filiale', max_length=30)),
                ('prefix_filiale', models.CharField(verbose_name='Préfix de codification', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalFormePharmaceutique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('forme', models.CharField(unique=True, verbose_name='Forme Pharmaceutique', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalFounisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('dossier', models.CharField(unique=True, verbose_name='Dossier fournisseur', max_length=10)),
                ('nom', models.CharField(unique=True, verbose_name='Fournisseur', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalLaboratoire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('dossier', models.CharField(unique=True, verbose_name='Dossier laboratoire', null=True, max_length=10)),
                ('nom', models.CharField(unique=True, verbose_name='Laboratoire', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalMotifsInventaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('motif_inventaire', models.CharField(verbose_name="Motif de l'inventaire", max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(unique=True, verbose_name='Code du produit', max_length=10)),
                ('produit', models.CharField(unique=True, verbose_name='Désignation du produit', max_length=50)),
                ('conditionnement', models.CharField(null=True, verbose_name='Conditionnement', blank=True, max_length=10)),
                ('poids', models.DecimalField(max_digits=10, verbose_name='Poids', default=0, blank=True, decimal_places=2)),
                ('volume', models.DecimalField(max_digits=10, verbose_name='Volume', default=0, blank=True, decimal_places=2)),
                ('poids_colis', models.DecimalField(max_digits=10, verbose_name='Poids colis', default=0, blank=True, decimal_places=2)),
                ('thermosensible', models.BooleanField(verbose_name='Produit thermolabile', default=False)),
                ('psychotrope', models.BooleanField(verbose_name='Produit psychotrope', default=False)),
                ('a_rique', models.BooleanField(verbose_name='Produit à risque', default=False)),
                ('dci', models.ForeignKey(verbose_name='DCI', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalDci', null=True)),
                ('laboratoire', models.ForeignKey(verbose_name='Laboratoire', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalLaboratoire', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalStatutDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('statut', models.CharField(unique=True, verbose_name='Statut Document', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalStatutProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('statut', models.CharField(unique=True, verbose_name='Statut produit', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalTransfertsEntreFiliale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('original_id', models.PositiveIntegerField(verbose_name='transfert original')),
                ('depuis_filiale', models.ForeignKey(verbose_name='Depuis filiale', related_name='depui_filiale', to='shared_data.GlobalFiliale', on_delete=django.db.models.deletion.PROTECT)),
                ('statut_doc', models.ForeignKey(verbose_name='Statut du transfert', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalStatutDocument')),
                ('vers_filiale', models.ForeignKey(verbose_name='Vers filiale', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalFiliale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlobalTypeEntreposage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type_entreposage', models.CharField(verbose_name="Types d'entreposage", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalTypesMouvementStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(unique=True, verbose_name='Type du mouvement', max_length=50)),
                ('niveau', models.SmallIntegerField(verbose_name='Niveau de difficulté', blank=True, null=True)),
                ('description', models.TextField(verbose_name='Description du mouvement', blank=True, null=True)),
                ('point_ligne_execution', models.SmallIntegerField(verbose_name='Points par ligne executée', blank=True, null=True)),
                ('point_ligne_saisie', models.SmallIntegerField(verbose_name='Points par ligne saisie', blank=True, null=True)),
                ('point_ligne_validation', models.SmallIntegerField(verbose_name='Points par ligne validée', blank=True, null=True)),
                ('point_boite_execution', models.SmallIntegerField(verbose_name='Points par boites executée', blank=True, null=True)),
                ('point_boite_validation', models.SmallIntegerField(verbose_name='Points par boite validée', blank=True, null=True)),
                ('point_colis_execution', models.SmallIntegerField(verbose_name='Points par colis executé', blank=True, null=True)),
                ('point_colis_validation', models.SmallIntegerField(verbose_name='Points par colis validée', blank=True, null=True)),
                ('point_colis_palettise_execution', models.SmallIntegerField(verbose_name='Point par colis palettisés executée', blank=True, null=True)),
                ('point_colis_palettise_validation', models.SmallIntegerField(verbose_name='Point par colis palettisé validé', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalWilaya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code_wilaya', models.PositiveSmallIntegerField(unique=True, verbose_name='Code Wilaya')),
                ('wilaya', models.CharField(unique=True, verbose_name='Nom de Wilaya', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='globaldetailstransfertentrefiliale',
            name='conformite',
            field=models.ForeignKey(verbose_name='Statut', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalStatutProduit'),
        ),
        migrations.AddField(
            model_name='globaldetailstransfertentrefiliale',
            name='entete',
            field=models.ForeignKey(to='shared_data.GlobalTransfertsEntreFiliale', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='globaldetailstransfertentrefiliale',
            name='produit',
            field=models.ForeignKey(verbose_name='Produit', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalProduit'),
        ),
        migrations.AddField(
            model_name='globaldci',
            name='forme_phrmaceutique',
            field=models.ForeignKey(verbose_name='Forme pharmaceutique', on_delete=django.db.models.deletion.PROTECT, to='shared_data.GlobalFormePharmaceutique'),
        ),
        migrations.AddField(
            model_name='globalcommune',
            name='wilaya',
            field=models.ForeignKey(verbose_name='Wilaya', blank=True, to='shared_data.GlobalWilaya', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='globalclient',
            name='commune',
            field=models.ForeignKey(verbose_name='Commune', blank=True, to='shared_data.GlobalCommune', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='globalaxe',
            name='filiale',
            field=models.ForeignKey(verbose_name='Filiale', to='shared_data.GlobalFiliale'),
        ),
    ]
