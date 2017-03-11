# -*- coding: utf-8 -*-
from django.db import models


class GlobalFiliale(models.Model):
    filiale = models.CharField(max_length=30, verbose_name='Nom de la filiale')
    prefix_filiale = models.CharField(max_length=10, verbose_name='Préfix de codification')


class GlobalAxe(models.Model):
    axe = models.CharField(max_length=50, verbose_name='Axe de livraion')
    filiale = models.ForeignKey(GlobalFiliale, verbose_name='Filiale')

    def __str__(self):
        return self.axe


class GlobalWilaya(models.Model):
    code_wilaya = models.PositiveSmallIntegerField(verbose_name='Code Wilaya', unique=True)
    wilaya = models.CharField(max_length=50, verbose_name='Nom de Wilaya', unique=True)

    def __str__(self):
        return ' '.join((self.code_wilaya.__str__(), self.wilaya))


class GlobalCommune(models.Model):
    code_commune = models.PositiveSmallIntegerField(verbose_name='Code', unique=True, null=True, blank=True)
    commune = models.CharField(max_length=50, verbose_name='Nom de la commune', unique=True)
    wilaya = models.ForeignKey(GlobalWilaya, verbose_name='Wilaya', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.commune


class GlobalClient(models.Model):
    dossier = models.CharField(max_length=20, verbose_name='Dossier Client', unique=True)
    nom_prenom = models.CharField(max_length=50, verbose_name='Nom Complet du client', unique=True)
    adresse = models.CharField(max_length=100, verbose_name='Adresse de livraion', null=True, blank=True)
    commune = models.ForeignKey(GlobalCommune, verbose_name='Commune', on_delete=models.PROTECT, null=True, blank=True)
    telephone = models.CharField(max_length=30, verbose_name='Téléphone', null=True, blank=True)

    def __str__(self):
        return ' '.join((self.dossier, '-', self.nom_prenom))


class GlobalStatutDocument(models.Model):
    statut = models.CharField(max_length=30, unique=True, verbose_name='Statut Document')

    def __str__(self):
        return self.statut


class GlobalStatutProduit(models.Model):
    statut = models.CharField(max_length=30, unique=True, verbose_name='Statut produit')

    def __str__(self):
        return self.statut


class GlobalFormePharmaceutique(models.Model):
    forme = models.CharField(max_length=30, unique=True, verbose_name='Forme Pharmaceutique')

    def __str__(self):
        return self.forme


class GlobalDci(models.Model):
    code_dci = models.CharField(max_length=30, unique=True, verbose_name='Code DCI')
    dci = models.CharField(max_length=50, verbose_name='DCI')
    forme_phrmaceutique = models.ForeignKey(GlobalFormePharmaceutique, verbose_name='Forme pharmaceutique',
                                            on_delete=models.PROTECT)
    dosage = models.CharField(max_length=20, verbose_name='Dosage')

    def __str__(self):
        return self.code_dci


class GlobalTypeEntreposage(models.Model):
    type_entreposage = models.CharField(max_length=50, verbose_name="Types d'entreposage")

    def __str__(self):
        return self.type_entreposage


class GlobalFounisseur(models.Model):
    dossier = models.CharField(max_length=10, unique=True, verbose_name='Dossier fournisseur')
    nom = models.CharField(max_length=50, unique=True, verbose_name='Fournisseur')

    def __str__(self):
        return ' '.join((self.dossier, self.nom))


class GlobalLaboratoire(models.Model):
    dossier = models.CharField(max_length=10, unique=True, verbose_name='Dossier laboratoire', null=True)
    nom = models.CharField(max_length=50, unique=True, verbose_name='Laboratoire')

    def __str__(self):
        return ' '.join((self.dossier, self.nom))


class GlobalProduit(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Code du produit')
    produit = models.CharField(max_length=50, unique=True, verbose_name='Désignation du produit')
    dci = models.ForeignKey(GlobalDci, verbose_name='DCI', null=True, on_delete=models.PROTECT)
    laboratoire = models.ForeignKey(GlobalLaboratoire, verbose_name='Laboratoire', null=True, on_delete=models.PROTECT)
    conditionnement = models.CharField(max_length=10, verbose_name='Conditionnement', null=True, blank=True)
    poids = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Poids', default=0, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Volume', default=0, blank=True)
    poids_colis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Poids colis', default=0,
                                      blank=True)
    thermosensible = models.BooleanField('Produit thermolabile', default=False)
    psychotrope = models.BooleanField(verbose_name='Produit psychotrope', default=False)
    a_rique = models.BooleanField(verbose_name='Produit à risque', default=False)

    def __str__(self):
        return self.produit


class GlobalTypesMouvementStock(models.Model):
    type = models.CharField(max_length=50, unique=True, verbose_name='Type du mouvement')
    niveau = models.SmallIntegerField(verbose_name='Niveau de difficulté', null=True, blank=True)
    description = models.TextField(verbose_name='Description du mouvement', null=True, blank=True)
    point_ligne_execution = models.SmallIntegerField(verbose_name='Points par ligne executée', null=True, blank=True)
    point_ligne_saisie = models.SmallIntegerField(verbose_name='Points par ligne saisie', null=True, blank=True)
    point_ligne_validation = models.SmallIntegerField(verbose_name='Points par ligne validée', null=True, blank=True)
    point_boite_execution = models.SmallIntegerField(verbose_name='Points par boites executée', null=True, blank=True)
    point_boite_validation = models.SmallIntegerField(verbose_name='Points par boite validée', null=True, blank=True)
    point_colis_execution = models.SmallIntegerField(verbose_name='Points par colis executé', null=True, blank=True)
    point_colis_validation = models.SmallIntegerField(verbose_name='Points par colis validée', null=True, blank=True)
    point_colis_palettise_execution = models.SmallIntegerField(verbose_name='Point par colis palettisés executée',
                                                               null=True, blank=True)
    point_colis_palettise_validation = models.SmallIntegerField(verbose_name='Point par colis palettisé validé',
                                                                null=True, blank=True)

    def __str__(self):
        return self.type


class GlobalMotifsInventaire(models.Model):
    motif_inventaire = models.CharField(max_length=30, verbose_name="Motif de l'inventaire")

    def __str__(self):
        return self.motif_inventaire


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GlobalTransfertsEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True)
    depuis_filiale = models.ForeignKey(GlobalFiliale, verbose_name='Depuis filiale', related_name='depui_filiale',
                                       on_delete=models.PROTECT)
    vers_filiale = models.ForeignKey(GlobalFiliale, verbose_name='Vers filiale', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(GlobalStatutDocument, verbose_name='Statut du transfert', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class GlobalDetailsTransfertEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True)
    entete = models.ForeignKey(GlobalTransfertsEntreFiliale, on_delete=models.PROTECT)
    conformite = models.ForeignKey(GlobalStatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    produit = models.ForeignKey(GlobalProduit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Vente HT')
    taux_tva = models.IntegerField(verbose_name='TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Lot')
    date_peremption = models.DateField(verbose_name='DDP')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite')
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite')
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis')
    qtt = models.IntegerField(verbose_name='Quantité')