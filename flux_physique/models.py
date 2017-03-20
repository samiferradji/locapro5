# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from refereces.models import StatutDocument, StatutProduit, Produit, Founisseur, Magasin, Emplacement, Client, \
    TypesMouvementStock, Employer, TypeEntreposage, Filiale
from shared_data.models import GlobalMotifsInventaire, GlobalTransfertsEntreFiliale, GlobalDetailsTransfertEntreFiliale


def get_current_year():
    current_year = datetime.datetime.now().year
    return current_year


exercice = get_current_year()


class Parametres(models.Model):
    filiale = models.ForeignKey(Filiale, verbose_name='Filiale')
    magasin_picking = models.ForeignKey(Magasin, verbose_name='Magasin de picking')
    emplacement_achat = models.ForeignKey(Emplacement, verbose_name='Emplacement de reception des achats')
    emplacement_expedition_transfert_entre_filiale = models.ForeignKey(
        Emplacement, verbose_name='Emplacement de reception des Transferts entre Filiales',
        related_name= 'emplacement_expedition_transfert_entre_filiale'
    )
    process_achat = models.ForeignKey(TypesMouvementStock, verbose_name='Processus achat', related_name='Achat')
    process_transfer = models.ForeignKey(TypesMouvementStock, verbose_name='Processus transfert interne',
                                         related_name='transfert_process')
    process_entreposage = models.ForeignKey(TypesMouvementStock, verbose_name='Processus entreposage',
                                            related_name='entreposage')
    process_etalage = models.ForeignKey(TypesMouvementStock, verbose_name='Processus etalage', related_name='etalage')
    process_vente_colis_complet = models.ForeignKey(TypesMouvementStock, verbose_name='Processus vente colis complets',
                                                    related_name='vente_colis')
    process_transfert_entre_filiales = models.ForeignKey(TypesMouvementStock,
                                                         verbose_name='Processus transfert entre filiales',
                                                    related_name='transfert_entre_filiales')
    process_expedition_transfert_entre_filiales = models.ForeignKey(TypesMouvementStock,
                                                         verbose_name='Processus extpédition des transferts entre '
                                                                      'filiales',
                                                         related_name='expedition_transfert_entre_filiales')
    process_reception_transfert_entre_filiales = models.ForeignKey(TypesMouvementStock,
                                                         verbose_name='Processus réception des transferts entre'
                                                                      ' filiales',
                                                         related_name='reception_transfert_entre_filiales')


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    class Meta:
        abstract = True


class AchatsFournisseur(BaseModel):
    fournisseur = models.ForeignKey(Founisseur, verbose_name='Fournissur', on_delete=models.PROTECT)
    n_BL = models.CharField(max_length=15, verbose_name='Numéro de BL')
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    date_entree = models.DateField(verbose_name='Date de BL')
    n_FAC = models.CharField(max_length=15, verbose_name="Numéro de Facture d'achat", null=True)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    observation = models.TextField(max_length=200, null=True)
    validate_by = models.ForeignKey(User, null=True, blank=True, related_name='validation_achats')

    def __str__(self):
        return self.n_BL

    class Meta:
        permissions = (
            ("valider_achats", "Peut valider les achats"),
            ("voir_historique_achats", "Peut voir l'historique des achats"),
            ("importer_achats", 'Peut importer les achats'),
        )


class DetailsAchatsFournisseur(BaseModel):
    entete = models.ForeignKey(AchatsFournisseur, on_delete=models.PROTECT)
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut Produit', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite', default=0)
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite', default=0)
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis', default=0)
    qtt = models.IntegerField(verbose_name='Quantité')
    ref_unique = models.CharField(max_length=20, verbose_name='reference_unique', default=0)


class CommandesClient(BaseModel):
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    n_commande = models.CharField(max_length=10, verbose_name='Numéro de commande')
    date_commande = models.DateField(verbose_name='Date de la commande')
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)


class DetailsCommandeClient(BaseModel):
    commande_client = models.ForeignKey(CommandesClient, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    qtt = models.IntegerField(verbose_name='Quantité')


class FacturesClient(BaseModel):
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.PROTECT)
    n_commande_original = models.CharField(max_length=10, verbose_name='Numéro de la commande', default=1)
    date_commande_original = models.DateField(verbose_name='Date de la commande', default=timezone.now)
    n_facrure = models.CharField(max_length=10, verbose_name='Numéro de facture', default=1)
    date_facture = models.DateField(verbose_name='Date facture', default=timezone.now)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)

    def __str__(self):
        return ' '.join((self.n_facrure, '/', str(self.curr_exercice)))


class DetailsFacturesClient(BaseModel):
    facture_client = models.ForeignKey(FacturesClient, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    qtt = models.IntegerField(verbose_name='Quantité')
    ref_unique = models.CharField(max_length=20, verbose_name='reference_unique', default=0)


class Transfert(BaseModel):
    depuis_magasin = models.ForeignKey(Magasin, verbose_name='Depuis magasin', related_name='+',
                                       on_delete=models.PROTECT)
    vers_magasin = models.ForeignKey(Magasin, verbose_name='Vers magasin', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    motif = models.ForeignKey(TypesMouvementStock, verbose_name='Motif du mouvement', default=1)
    validate_by = models.ForeignKey(User, null=True, blank=True, related_name='validation_name')

    def __str__(self):
        return str(self.id)

    class Meta:
        permissions = (
            ("valider_mouvements_stock", "Peut valider les mouvements de stocks"),
            ("transferer", "Peut transferer"),
            ("entreposer", "Peut Entreposer"),
            ("voir_historique_transferts", "Peut voir l'historique des transferts"),
            ("voir_stock", "Peut voir l'état du stock"),
            ("exporter_stock", "Peut exporter l'état du stock"),
            ("sortie_colis_complets", "Peut fair des sorties en colis d'origine"),
        )


class Stock(BaseModel):
    id_in_content_type = models.CharField(max_length=20, verbose_name='Original id')
    content_type = models.PositiveIntegerField(verbose_name='Contenent_type')
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Vente HT')
    taux_tva = models.IntegerField(verbose_name='TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Lot')
    date_peremption = models.DateField(verbose_name='DDP')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite', default=0)
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite', default=0)
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis', default=0)
    qtt = models.IntegerField(verbose_name='Quantité')
    motif = models.CharField(max_length=20, verbose_name='Transaction')
    recu = models.BooleanField(default=False, verbose_name='Reçu')


class DetailsTransfert(BaseModel):
    entete = models.ForeignKey(Transfert, on_delete=models.PROTECT)
    id_in_content_type = models.PositiveIntegerField(verbose_name='Id in content type')
    content_type = models.PositiveIntegerField(verbose_name='Contenent_type')
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    depuis_emplacement = models.ForeignKey(Emplacement, verbose_name='Depuis Empl', on_delete=models.PROTECT,
                                           related_name='depuis_empl')
    vers_emplacement = models.ForeignKey(Emplacement, verbose_name='Vers Empl', on_delete=models.PROTECT,
                                         related_name='vers_empl')
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
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


class MotifsInventaire(models.Model):
    motif_inventaire = models.CharField(max_length=30, verbose_name="Motif de l'inventaire")

    def __str__(self):
        return self.motif_inventaire


class Inventaire(BaseModel):
    motif_inventaire = models.ForeignKey(MotifsInventaire, verbose_name="Motif de l'inventaire",
                                         on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, verbose_name='Description')

    def __str__(self):
        return ' '.join(
            (self.motif_inventaire.__str__(), '-', str(self.id)))


class DetailsInventaire(BaseModel):
    entete = models.ForeignKey(Inventaire, on_delete=models.PROTECT)
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut Produit', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite')
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite')
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis')
    qtt = models.IntegerField(verbose_name='Quantité')

    def __str__(self):
        return str(self.id)


class EnteteTempo(BaseModel):
    transaction = models.CharField(max_length=30)


class Reservation(models.Model):
    entete_tempo = models.ForeignKey(EnteteTempo, on_delete=models.CASCADE, verbose_name='Entête de la réservation')
    id_stock = models.ForeignKey(Stock, verbose_name='Id Stock')
    qtt = models.IntegerField(verbose_name='Quantité réservée')
    new_emplacement = models.ForeignKey(Emplacement, null=True)


class Validation(BaseModel):
    id_in_content_type = models.CharField(max_length=20, verbose_name='Id in content type')
    content_type = models.PositiveIntegerField(verbose_name='Contenent type')
    boite_count = models.IntegerField(verbose_name='Nombre de boites')
    boites_en_vrac = models.IntegerField(verbose_name='Nombre de boites en VRAC', default=0)
    ligne_count = models.IntegerField(verbose_name='Nombre de lignes')
    colis_count = models.IntegerField(verbose_name='Nombre de colis', default=0)
    colis_en_palette = models.IntegerField(verbose_name='Nombre de colis palettisés', default=0)
    motif_mvnt = models.ForeignKey(TypesMouvementStock, verbose_name='Motif du mouvement de stock', default=1)
    origin_created_date = models.DateTimeField(default=timezone.now)
    origine_created_by = models.ForeignKey(User, related_name='user_creat_Bon', default=2)

    def __str__(self):
        return ' '.join((str(self.id_in_content_type), str(self.content_type)))


class HistoriqueDuTravail(models.Model):
    id_validation = models.ForeignKey(Validation, on_delete=models.CASCADE, verbose_name='ID Validation')
    employer = models.ForeignKey(Employer, verbose_name='Employé', on_delete=models.PROTECT)
    groupe = models.SmallIntegerField(verbose_name='Effectif du groupe')

    def __str__(self):
        return ' '.join(
            (self.employer.__str__(), self.groupe.__str__())
        )


class TransfertsEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    depuis_filiale = models.ForeignKey(Filiale, verbose_name='Depuis filiale', related_name='depui_filiale',
                                       on_delete=models.PROTECT)
    vers_filiale = models.ForeignKey(Filiale, verbose_name='Vers filiale', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du transfert', on_delete=models.PROTECT)
    nombre_colis = models.PositiveSmallIntegerField(verbose_name='Nombre de colis T° ambiante')
    nombre_colis_frigo = models.PositiveSmallIntegerField(verbose_name='Nombre de colis T° 2 à 8°C')

    class Meta:
        permissions = (
            ("ajouter_tef", "Peut ajouter transferts entre filiale"),
            ("confirmer_tef", "Peut confirmer transferts entre filiale"),
            ("expedier_tef", "Peut expédier transferts entre filiale"),
            ("recevoir_tef", "Peut recevoir transferts entre filiale"),
            ("voir_historique", "Peut voire l'historique des transferts entre filiale"),
        )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            curent_filiale= Parametres.objects.get(id=1)
            i = TransfertsEntreFiliale.objects.filter(depuis_filiale=curent_filiale.filiale).count()
            self._id = i + 1
            self.id = '-'.join((str(get_current_year()), curent_filiale.filiale.prefix_filiale, str(self._id)))
        super(TransfertsEntreFiliale, self).save(*args, **kwargs)


class DetailsTransfertEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    entete = models.ForeignKey(TransfertsEntreFiliale, on_delete=models.PROTECT)
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
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
    depuis_emplacement = models.ForeignKey(Emplacement, verbose_name='Depuis Empl', on_delete=models.PROTECT,
                                           related_name='depuis_empl_G')
    vers_emplacement = models.ForeignKey(Emplacement, verbose_name='Vers Empl', on_delete=models.PROTECT,
                                         related_name='vers_empl_G')

    def save(self, *args, **kwargs):
        if not self.id:
            curent_filiale= Parametres.objects.get(id=1)
            i = DetailsTransfertEntreFiliale.objects.filter(entete__depuis_filiale=curent_filiale.filiale).count()
            self._id = i + 1
            self.id = '-'.join((str(get_current_year()), curent_filiale.filiale.prefix_filiale, str(self._id)))
        super(DetailsTransfertEntreFiliale, self).save(*args, **kwargs)


class ExpeditionTransfertsEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    vers_filiale = models.ForeignKey(Filiale, verbose_name='Vers filiale', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du transfert', on_delete=models.PROTECT)
    livreur = models.CharField(max_length=50, verbose_name='Livreur ou démarcheur')
    fourgon = models.CharField(max_length=15, verbose_name='Immatriculation du véhicule')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            curent_filiale= Parametres.objects.get(id=1)
            i = ExpeditionTransfertsEntreFiliale.objects.all().count()
            self._id = i + 1
            self.id = '-'.join((str(get_current_year()), curent_filiale.filiale.prefix_filiale, str(self._id)))
        super(ExpeditionTransfertsEntreFiliale, self).save(*args, **kwargs)

class DetailsExpeditionTransfertsEntreFiliale(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    entete = models.ForeignKey(ExpeditionTransfertsEntreFiliale, verbose_name='Entete', on_delete=models.PROTECT)
    transfert = models.ForeignKey(TransfertsEntreFiliale, verbose_name='N° du transfert')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            i = DetailsExpeditionTransfertsEntreFiliale.objects.all().count()
            self._id = i + 1
            currrent_filiale = Parametres.objects.get(id=1).filiale.prefix_filiale
            self.id = '-'.join((currrent_filiale, str(self._id)))
        super(DetailsExpeditionTransfertsEntreFiliale, self).save(*args, **kwargs)


def get_current_filiale_prefix():
    current_prefix = Parametres.objects.get(id=1).filiale.prefix_filiale
    return str(current_prefix)

@receiver(post_save, sender=DetailsAchatsFournisseur, dispatch_uid="add_achats_to_stock")
def add_achat_to_stock(sender, instance, created, **kwargs):
    if created is True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt = instance.qtt
        new_motif = 'Achat'
        new_created_by = instance.created_by

        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by=new_created_by
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsAchatsFournisseur, dispatch_uid="delete_achat_from_stock")
def delete_achat_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@transaction.atomic
@receiver(post_save, sender=DetailsTransfert, dispatch_uid="add_transfert_to_stock")
def add_transfert_to_stock(sender, instance, created, **kwargs):
    if created is True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.vers_emplacement
        old_emplacement = instance.depuis_emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt_in = instance.qtt
        new_motif = 'Transfert-In'
        new_created_by = instance.created_by
        new_obj1 = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt_in, motif=new_motif,
            created_by=new_created_by
        )

        new_qtt_out = -1 * instance.qtt
        new_motif = 'Transfert-Out '
        new_obj2 = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=old_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt_out, motif=new_motif,
            created_by=new_created_by
        )
        new_obj1.save()
        new_obj2.save()


@receiver(post_delete, sender=DetailsTransfert, dispatch_uid="delete_transfert_from_stock")
def delete_transfert_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.filter(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@transaction.atomic
@receiver(post_save, sender=DetailsFacturesClient, dispatch_uid="add_achats_to_stock")
def add_vente_to_stock(sender, instance, created, **kwargs):
    if created is True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = StatutProduit.objects.get(statut='Conforme')
        new_emplacement = instance.produit.prelevement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.produit.poids
        new_volume_boite = instance.produit.volume
        new_poids_colis = 0
        new_qtt = -1 * instance.qtt
        new_motif = 'Vente'
        new_created_by = instance.created_by
        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by=new_created_by, recu=True
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsFacturesClient, dispatch_uid="delete_achat_from_stock")
def delete_vente_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@receiver(post_save, sender=DetailsInventaire, dispatch_uid="add_inventaire_to_stock")
def add_inventaire_to_stock(sender, instance, created, **kwargs):
    if created is True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt = instance.qtt
        new_motif = 'Inventaire'
        new_created_by = instance.created_by

        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by=new_created_by
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsInventaire, dispatch_uid="delete_inventaire_from_stock")
def delete_inventaire_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@receiver(post_save, sender=Transfert, dispatch_uid="add_validation_transfert")
def add_validation_mvt_stock(sender, instance, created, **kwargs):
    if created is False:
        if instance.statut_doc_id == 2:
            contenent_type = ContentType.objects.get_for_model(instance).id
            id_in_content_type = instance.id
            linges_count = DetailsTransfert.objects.filter(entete=instance.id).count()
            boites_aggregaion = DetailsTransfert.objects.filter(entete=instance.id).aggregate(Sum('qtt'))
            lignes_transfert = DetailsTransfert.objects.filter(entete=instance.id)
            total_qtt = boites_aggregaion['qtt__sum']
            type_mouvement = instance.motif
            created_by = instance.validate_by
            colis = 0
            colis_en_palette = 0
            vrac = 0
            for line in lignes_transfert:
                if line.colisage != 0:
                    if instance.motif in [Parametres.objects.get(id=1).process_entreposage,
                                          Parametres.objects.get(id=1).process_etalage]:
                        if line.vers_emplacement.type_entreposage_id == 1:
                            vrac += line.qtt
                        if line.vers_emplacement.type_entreposage_id == 2:
                            vrac += line.qtt % line.colisage
                            colis += line.qtt // line.colisage
                        if line.vers_emplacement.type_entreposage_id == 3:
                            vrac += line.qtt % line.colisage
                            colis_en_palette += line.qtt // line.colisage
                    else:
                        if line.depuis_emplacement.type_entreposage_id == 1:
                            vrac += line.qtt
                        if line.depuis_emplacement.type_entreposage_id == 2:
                            vrac += line.qtt % line.colisage
                            colis += line.qtt // line.colisage
                        if line.depuis_emplacement.type_entreposage_id == 3:
                            vrac += line.qtt % line.colisage
                            colis_en_palette += line.qtt // line.colisage
                else:
                    vrac += line.qtt
            validation_check = Validation.objects.filter(
                content_type=contenent_type,
                id_in_content_type=id_in_content_type
            )
            if validation_check.exists():
                pass
            else:
                obj = Validation(
                    content_type=contenent_type,
                    id_in_content_type=id_in_content_type,
                    ligne_count=linges_count,
                    boite_count=total_qtt,
                    boites_en_vrac=vrac,
                    colis_count=colis,
                    colis_en_palette=colis_en_palette,
                    motif_mvnt=type_mouvement,
                    created_by=created_by,
                    origin_created_date=instance.created_date,
                    origine_created_by=instance.created_by
                )
                obj.save()


@receiver(post_save, sender=AchatsFournisseur, dispatch_uid="add_validation_reception")
def add_validation_reception(sender, instance, created, **kwargs):
    if created is False:
        if instance.statut_doc_id == 2:
            contenent_type = ContentType.objects.get_for_model(instance).id
            id_in_content_type = instance.id
            linges_count = DetailsAchatsFournisseur.objects.filter(entete=instance.id).count()
            boites_aggregaion = DetailsAchatsFournisseur.objects.filter(entete=instance.id).aggregate(Sum('qtt'))
            lignes_achat = DetailsAchatsFournisseur.objects.filter(entete=instance.id)
            total_qtt = boites_aggregaion['qtt__sum']
            type_mouvement = Parametres.objects.get(id=1).process_achat
            created_by = instance.validate_by
            colis = 0
            colis_en_palette = 0
            vrac = 0
            for line in lignes_achat:
                if line.colisage != 0:
                    vrac += line.qtt % line.colisage
                    colis += line.qtt // line.colisage
                else:
                    vrac += line.qtt
            validation_check = Validation.objects.filter(
                content_type=contenent_type,
                id_in_content_type=id_in_content_type
            )
            if validation_check.exists():
                pass
            else:
                obj = Validation(
                    content_type=contenent_type,
                    id_in_content_type=id_in_content_type,
                    ligne_count=linges_count,
                    boite_count=total_qtt,
                    boites_en_vrac=vrac,
                    colis_count=colis,
                    colis_en_palette=colis_en_palette,
                    motif_mvnt=type_mouvement,
                    created_by=created_by,
                    origin_created_date=instance.created_date,
                    origine_created_by=instance.created_by
                )
                obj.save()


@receiver(post_save, sender=Inventaire, dispatch_uid="add_validation_inventaire")
def add_validation_inventaire(sender, instance, created, **kwargs):
    if created is False:
        if instance.statut_doc_id == 2:
            contenent_type = ContentType.objects.get_for_model(DetailsInventaire).id
            lignes_inventaire = DetailsInventaire.objects.filter(entete=instance.id)
            for item in lignes_inventaire:
                stock_item = Stock.objects.get(id_in_content_type=item.id, content_type=contenent_type)
                stock_item.recu = True
                stock_item.save()


@receiver(post_save, sender=MotifsInventaire, dispatch_uid="add_motif_inventaire_stockinstance")
def add_motif_inventaire_to_global_data(sender, instance, created, **kwargs):
    if created:
        new_obj = GlobalMotifsInventaire(id=instance.id,
                                         motif_inventaire=instance.motif_inventaire
                                         )
        new_obj.save()


# ********************* Signals for transfer between filiales **************************

@receiver(post_save, sender=DetailsTransfertEntreFiliale, dispatch_uid="add_trandferts_entre_filiale_to_stock")
def add_transfert_entre_filiale_to_stock(sender, instance, created, **kwargs):
    if created is True:
        current_filiale = Parametres.objects.get(id=1).filiale
        if instance.entete.depuis_filiale_id == current_filiale.id:
            if instance.entete.vers_filiale_id != current_filiale.id:
                new_id_stock = instance.id
                new_contenent_type = ContentType.objects.get_for_model(instance).id
                new_conformite = instance.conformite
                new_emplacement_id = Parametres.objects.get(id=1).emplacement_achat_id
                new_produit = instance.produit
                new_prix_achat = instance.prix_achat
                new_prix_vente = instance.prix_vente
                new_taux_tva = instance.taux_tva
                new_shp = instance.shp
                new_ppa_ht = instance.ppa_ht
                new_n_lot = instance.n_lot
                new_date_peremption = instance.date_peremption
                new_colisage = instance.colisage
                new_poids_boite = instance.poids_boite
                new_volume_boite = instance.volume_boite
                new_poids_colis = instance.poids_colis
                new_qtt = instance.qtt * -1
                new_motif = 'Cession-Out'
                new_created_by = instance.created_by
                new_obj = Stock(
                    id_in_content_type=new_id_stock, content_type=new_contenent_type,
                    conformite=new_conformite, emplacement_id=new_emplacement_id, produit=new_produit,
                    prix_achat=new_prix_achat, prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp,
                    ppa_ht=new_ppa_ht, n_lot=new_n_lot, date_peremption=new_date_peremption, colisage=new_colisage,
                    poids_boite=new_poids_boite, volume_boite=new_volume_boite, poids_colis=new_poids_colis,
                    qtt=new_qtt, motif=new_motif, created_by=new_created_by
                )
                new_obj.save()


@receiver(post_delete, sender=DetailsTransfertEntreFiliale, dispatch_uid="delete_transfert_entre_filiale_from_stock")
def delete_transfert_entre_filiale_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    if __name__ == '__main__':
        if obj:
            obj.delete()
            #  En cas de supression d'une ligne de transfert entre filiale, il faux supprimer manuellment dans :
            #  1 - Lignes transfert de toutes les filiale
            #  2 - Lignes transfert dans global data
            #  Et cela impérativement pendant que toutes les filiale sont déconnecté de locapro


@receiver(post_save, sender=TransfertsEntreFiliale, dispatch_uid="validate_transfert_entre_filiale")
def validate_transfert_entre_filiale(sender, instance, created, **kwargs):
    if created is False:
        if instance.statut_doc_id == 2:  # 2 to for the statut Conformé
            if GlobalTransfertsEntreFiliale.objects.filter(id=instance.id).exists():
                pass  # Transfer already synchronised
            else:
                if instance.depuis_filiale_id == Parametres.objects.get(id=1).filiale_id:
                    if instance.vers_filiale_id != Parametres.objects.get(id=1).filiale_id:
                        transfert_details = DetailsTransfertEntreFiliale.objects.filter(entete_id=instance.id).all()
                        # Validate inventory outbound flow (recu = True)
                        for line in transfert_details:
                            stock_obj = Stock.objects.get(id_in_content_type=line.id)
                            stock_obj.recu = True
                            stock_obj.save()
                        #  Add validation for Effort-statistics

                        contenent_type = ContentType.objects.get_for_model(instance).id
                        id_in_content_type = instance.id
                        linges_count = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id).count()
                        boites_aggregaion = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id
                                                                                        ).aggregate(Sum('qtt'))
                        lignes_transfert = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id)
                        total_qtt = boites_aggregaion['qtt__sum']
                        type_mouvement = Parametres.objects.get(id=1).process_transfert_entre_filiales
                        created_by = 1  # 1 pour Admin
                        colis = 0
                        colis_en_palette = 0
                        vrac = 0
                        for line in lignes_transfert:
                            if line.colisage != 0:
                                if line.depuis_emplacement.type_entreposage_id == 1:
                                    vrac += line.qtt
                                elif line.depuis_emplacement.type_entreposage_id == 2:
                                    vrac += line.qtt % line.colisage
                                    colis += line.qtt // line.colisage
                                elif line.depuis_emplacement.type_entreposage_id == 3:
                                    vrac += line.qtt % line.colisage
                                    colis_en_palette += line.qtt // line.colisage
                            else:
                                vrac += line.qtt
                        validation_check = Validation.objects.filter(
                            content_type=contenent_type,
                            id_in_content_type=id_in_content_type
                        )
                        if validation_check.exists():
                            pass
                        else:
                            obj = Validation(
                                content_type=contenent_type,
                                id_in_content_type=id_in_content_type,
                                ligne_count=linges_count,
                                boite_count=total_qtt,
                                boites_en_vrac=vrac,
                                colis_count=colis,
                                colis_en_palette=colis_en_palette,
                                motif_mvnt=type_mouvement,
                                created_by_id=created_by,
                                origin_created_date=instance.created_date,
                                origine_created_by=instance.created_by
                            )
                            obj.save()

                        #  Add validated transfer to Global-transfert-entre-filiale
                        details_transfert_entre_filiale = DetailsTransfertEntreFiliale.objects.filter(
                            entete=instance.id).all()
                        new_gtef_obj = GlobalTransfertsEntreFiliale(
                            id=instance.id,
                            depuis_filiale_id=instance.depuis_filiale_id,
                            vers_filiale_id=instance.vers_filiale_id,
                            statut_doc_id=2,
                            nombre_colis=instance.nombre_colis,
                            nombre_colis_frigo=instance.nombre_colis_frigo
                            )
                        new_gtef_obj.save()
                        for obj in details_transfert_entre_filiale:
                            new_line = GlobalDetailsTransfertEntreFiliale(
                                    id=obj.id,
                                    entete_id=new_gtef_obj.id,
                                    conformite_id=obj.conformite_id,
                                    produit_id=obj.produit_id,
                                    prix_achat=obj.prix_achat,
                                    prix_vente=obj.prix_vente,
                                    taux_tva=obj.taux_tva,
                                    shp=obj.shp,
                                    ppa_ht=obj.ppa_ht,
                                    n_lot=obj.n_lot,
                                    date_peremption=obj.date_peremption,
                                    colisage=obj.colisage,
                                    poids_boite=obj.poids_boite,
                                    volume_boite=obj.volume_boite,
                                    poids_colis=obj.poids_colis,
                                    qtt=obj.qtt,
                                )
                            new_line.save()
                    else:
                        pass
                else:
                    pass

        elif instance.statut_doc_id == 3:  # 3 for the status Expédié
            if GlobalTransfertsEntreFiliale.objects.filter(id=instance.id).exists():
                current_obj = GlobalTransfertsEntreFiliale.objects.get(id=instance.id)
                if instance.depuis_filiale_id == Parametres.objects.get(id=1).filiale_id:
                    if instance.vers_filiale_id != Parametres.objects.get(id=1).filiale_id:
                        if current_obj.statut_doc_id != 3:
                            current_obj.statut_doc_id = 3
                            current_obj.save()
                            # TODO signal for expédier , instance new expédition confirmed
            else:
                pass
        elif instance.statut_doc_id == 4:  # 4 to for the status Recu
            if GlobalTransfertsEntreFiliale.objects.filter(id=instance.id).exists():
                current_obj = GlobalTransfertsEntreFiliale.objects.get(id=instance.id)
                if instance.depuis_filiale_id != Parametres.objects.get(id=1).filiale_id:
                    if instance.vers_filiale_id == Parametres.objects.get(id=1).filiale_id:
                        if current_obj.statut_doc_id != 4:
                            current_obj.statut_doc_id = 4
                            current_obj.save()
                            ligne_transfert = DetailsTransfertEntreFiliale.objects.filter(entete_id=instance.id)
                            for line in ligne_transfert:
                                if Stock.objects.filter(id_in_content_type=line.id).exists():
                                    pass
                                else:
                                    new_id_stock = line.id
                                    new_contenent_type = ContentType.objects.get_for_model(line).id
                                    new_conformite_id = line.conformite_id
                                    new_emplacement_id = Parametres.objects.get(id=1).emplacement_achat_id
                                    new_produit = line.produit
                                    new_prix_achat = line.prix_achat
                                    new_prix_vente = line.prix_vente
                                    new_taux_tva = line.taux_tva
                                    new_shp = line.shp
                                    new_ppa_ht = line.ppa_ht
                                    new_n_lot = line.n_lot
                                    new_date_peremption = line.date_peremption
                                    new_colisage = line.colisage
                                    new_poids_boite = line.poids_boite
                                    new_volume_boite = line.volume_boite
                                    new_poids_colis = line.poids_colis
                                    new_qtt = line.qtt
                                    new_motif = 'Cession-In'
                                    new_created_by = line.created_by
                                    new_obj = Stock(
                                        id_in_content_type=new_id_stock, content_type=new_contenent_type,
                                        conformite_id=new_conformite_id, emplacement_id=new_emplacement_id,
                                        produit=new_produit,
                                        prix_achat=new_prix_achat, prix_vente=new_prix_vente, taux_tva=new_taux_tva,
                                        shp=new_shp,
                                        ppa_ht=new_ppa_ht, n_lot=new_n_lot, date_peremption=new_date_peremption,
                                        colisage=new_colisage, poids_boite=new_poids_boite, volume_boite=new_volume_boite,
                                        poids_colis=new_poids_colis, qtt=new_qtt, recu=True, motif=new_motif,
                                        created_by=new_created_by
                                    )
                                    new_obj.save()

                            # Add validation for Effort-statistics

                            contenent_type = ContentType.objects.get_for_model(instance).id
                            id_in_content_type = instance.id
                            linges_count = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id).count()
                            boites_aggregaion = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id
                                                                                            ).aggregate(Sum('qtt'))
                            lignes_transfert = DetailsTransfertEntreFiliale.objects.filter(entete=instance.id)
                            total_qtt = boites_aggregaion['qtt__sum']
                            type_mouvement = Parametres.objects.get(id=1).process_reception_transfert_entre_filiales
                            created_by = 1  # 1 pour Admin
                            colis = 0
                            colis_en_palette = 0
                            vrac = 0
                            for line in lignes_transfert:
                                if line.colisage != 0:
                                    vrac += line.qtt % line.colisage
                                    colis += line.qtt // line.colisage
                                else:
                                    vrac += line.qtt
                            validation_check = Validation.objects.filter(
                                content_type=contenent_type,
                                id_in_content_type=id_in_content_type
                            )
                            if validation_check.exists():
                                pass
                            else:
                                obj = Validation(
                                    content_type=contenent_type,
                                    id_in_content_type=id_in_content_type,
                                    ligne_count=linges_count,
                                    boite_count=total_qtt,
                                    boites_en_vrac=vrac,
                                    colis_count=colis,
                                    colis_en_palette=colis_en_palette,
                                    motif_mvnt=type_mouvement,
                                    created_by_id=created_by,
                                    origin_created_date=instance.created_date,
                                    origine_created_by=instance.created_by
                                )
                                obj.save()