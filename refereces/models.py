# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Axe(models.Model):
    axe = models.CharField(max_length=50, verbose_name='Axe de livraion', unique=True)

    def __str__(self):
        return self.axe


class Wilaya(models.Model):
    code_wilaya = models.PositiveSmallIntegerField(verbose_name='Code Wilaya', unique=True)
    wilaya = models.CharField(max_length=50, verbose_name='Nom de Wilaya', unique=True)

    def __str__(self):
        return ' '.join((self.code_wilaya.__str__(), self.wilaya))


class Commune(models.Model):
    code_commune = models.PositiveSmallIntegerField(verbose_name='Code', unique=True, null=True, blank=True)
    commune = models.CharField(max_length=50, verbose_name='Nom de la commune', unique=True)
    wilaya = models.ForeignKey(Wilaya, verbose_name='Wilaya', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.commune


class Client(models.Model):
    dossier = models.CharField(max_length=20, verbose_name='Dossier Client', unique=True)
    nom_prenom = models.CharField(max_length=50, verbose_name='Nom Complet du client', unique=True)
    adresse = models.CharField(max_length=100, verbose_name='Adresse de livraion', null=True, blank=True)
    commune = models.ForeignKey(Commune, verbose_name='Commune', on_delete=models.PROTECT, null=True, blank=True)
    axe = models.ForeignKey(Axe, verbose_name='Axe de livaion', on_delete=models.PROTECT, null=True, blank=True)
    telephone = models.CharField(max_length=30, verbose_name='Téléphone', null=True, blank=True)

    def __str__(self):
        return ' '.join((self.dossier, '-', self.nom_prenom))


class StatutDocument(models.Model):
    statut = models.CharField(max_length=30, unique=True, verbose_name='Statut Document')

    def __str__(self):
        return self.statut


class StatutProduit(models.Model):
    statut = models.CharField(max_length=30, unique=True, verbose_name='Statut produit')

    def __str__(self):
        return self.statut


class FormePharmaceutique(models.Model):
    forme = models.CharField(max_length=30, unique=True, verbose_name='Forme Pharmaceutique')

    def __str__(self):
        return self.forme


class Dci(models.Model):
    code_dci = models.CharField(max_length=30, unique=True, verbose_name='Code DCI')
    dci = models.CharField(max_length=50, verbose_name='DCI')
    forme_phrmaceutique = models.ForeignKey(FormePharmaceutique, verbose_name='Forme pharmaceutique',
                                            on_delete=models.PROTECT)
    dosage = models.CharField(max_length=20, verbose_name='Dosage')

    def __str__(self):
        return self.code_dci


class TypeEntreposage(models.Model):
    type_entreposage = models.CharField(max_length=50, verbose_name="Types d'entreposage")

    def __str__(self):
        return self.type_entreposage


class Magasin(models.Model):
    magasin = models.CharField(max_length=30, unique=True, verbose_name='Magasin')
    type_entreposage = models.ForeignKey(TypeEntreposage, default=1, verbose_name="Type d'entreposage principal")

    def __str__(self):
        return self.magasin


class Emplacement(models.Model):
    emplacement = models.CharField(max_length=10, unique=True, verbose_name='Emplacement')
    magasin = models.ForeignKey(Magasin, verbose_name='Magasin', on_delete=models.PROTECT)
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Capacité en volume', null=True)
    poids = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Charge Maximale', null=True)
    type_entreposage = models.ForeignKey(TypeEntreposage, default=1, verbose_name="Type d'entreposage")

    def __str__(self):
        return ' '.join((self.emplacement, self.magasin.__str__(), '--', str(self.type_entreposage)))


class Founisseur(models.Model):
    dossier = models.CharField(max_length=10, unique=True, verbose_name='Dossier fournisseur')
    nom = models.CharField(max_length=50, unique=True, verbose_name='Fournisseur')

    def __str__(self):
        return ' '.join((self.dossier, self.nom))


class Laboratoire(models.Model):
    dossier = models.CharField(max_length=10, unique=True, verbose_name='Dossier laboratoire', null=True)
    nom = models.CharField(max_length=50, unique=True, verbose_name='Laboratoire')

    def __str__(self):
        return ' '.join((self.dossier, self.nom))


class Produit(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Code du produit')
    produit = models.CharField(max_length=50, unique=True, verbose_name='Désignation du produit')
    dci = models.ForeignKey(Dci, verbose_name='DCI', null=True, on_delete=models.PROTECT)
    laboratoire = models.ForeignKey(Laboratoire, verbose_name='Laboratoire', null=True, on_delete=models.PROTECT)
    conditionnement = models.CharField(max_length=10, verbose_name='Conditionnement', null=True, blank=True)
    poids = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Poids', default=0, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Volume', default=0, blank=True)
    poids_colis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Poids colis', default=0,
                                      blank=True)
    thermosensible = models.BooleanField('Produit thermolabile', default=False)
    psychotrope = models.BooleanField(verbose_name='Produit psychotrope', default=False)
    a_rique = models.BooleanField(verbose_name='Produit à risque', default=False)
    prelevement = models.ForeignKey(Emplacement, verbose_name='Emplacement de prélèvement', null=True,
                                    on_delete=models.PROTECT, default=1)
    seuil_min = models.IntegerField(verbose_name='Stock Min', default=50)
    seuil_max = models.IntegerField(verbose_name='Stock MAx', default=200)
    type_entreposage = models.ForeignKey(TypeEntreposage, null=True, blank=True)

    def __str__(self):
        return self.produit


class TypesMouvementStock(models.Model):
    type = models.CharField(max_length=50, unique=True, verbose_name='Type du mouvement')
    niveau = models.SmallIntegerField(verbose_name='Niveau de difficulté')
    description = models.TextField(verbose_name='Description du mouvement', null=True)

    def __str__(self):
        return self.type


class Employer(models.Model):
    code_RH = models.CharField(max_length=10, verbose_name='Code RH', unique=True)
    nom = models.CharField(max_length=50, verbose_name='Nom et prénom')

    class Meta:
        ordering = ['nom', ]

    def __str__(self):
        return ' '.join((self.nom,self.code_RH))


class DepuisMagasinsAutorise(models.Model):
    user = models.ForeignKey(User, verbose_name='Utilisateur')
    magasins = models.ForeignKey(Magasin, verbose_name='Depuis : Magasins Autorisés')


class VersMagasinsAutorise(models.Model):
    user = models.ForeignKey(User, verbose_name='Utilisateur')
    magasins = models.ForeignKey(Magasin, verbose_name='Vers : Magasins Autorisés')


class StatutsAutorise(models.Model):
    user = models.ForeignKey(User, verbose_name='Utilisateur')
    statuts = models.ForeignKey(StatutProduit, verbose_name='Statuts Autorisés')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    code_employee = models.ForeignKey(Employer, verbose_name='Code Employé')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Magasin, dispatch_uid="add_emplacement_instance")
def auto_add_emplacement_instance(sender, instance, created, **kwargs):
    if created == True:
        emplacemet = 'Inst-' + str(instance.id)
        magasin = instance
        poids = 0
        volume = 0
        obj = Emplacement(
            emplacement=emplacemet,
            magasin=magasin,
            poids=poids,
            volume=volume,
            type_entreposage=instance.type_entreposage
            )
        obj.save()
