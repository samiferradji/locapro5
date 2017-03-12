from django.shortcuts import render
from .models import GlobalFiliale, GlobalAxe, GlobalWilaya, GlobalCommune, GlobalClient, GlobalStatutDocument, \
    GlobalStatutProduit, GlobalFormePharmaceutique, GlobalDci, GlobalTypeEntreposage, GlobalFounisseur,\
    GlobalLaboratoire, GlobalProduit, GlobalTypesMouvementStock, GlobalMotifsInventaire
from refereces.models import Filiale, Axe, Wilaya, Commune, Client, StatutDocument, StatutProduit, \
    FormePharmaceutique, Dci, TypeEntreposage, Founisseur, Laboratoire, Produit , TypesMouvementStock
from flux_physique.models import MotifsInventaire


def synch_data(request):

    def sync_filiale():
        global_objs = GlobalFiliale.objects.all()
        for obj in global_objs:
            if Filiale.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Filiale(id=obj.id,
                                  filiale=obj.filiale,
                                  prefix_filiale=obj.prefix_filiale)
                new_obj.save()

    def sync_axe():
        global_objs = GlobalAxe.objects.all()
        for obj in global_objs:
            if Axe.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Axe(id=obj.id,
                              axe=obj.axe)
                new_obj.save()

    def sync_wilaya():
        global_objs = GlobalWilaya.objects.all()
        for obj in global_objs:
            if Wilaya.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Wilaya(id=obj.id,
                                 code_wilaya=obj.code_wilaya,
                                 wilaya=obj.wilaya
                                 )
                new_obj.save()

    def sync_commune():
        global_objs = GlobalCommune.objects.all()
        for obj in global_objs:
            if Commune.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Commune(id=obj.id,
                                  code_commune=obj.code_commune,
                                  commune=obj.commune,
                                  wilaya_id=obj.wilaya.id
                                  )
                new_obj.save()

    def sync_client():
        global_objs = GlobalClient.objects.all()
        for obj in global_objs:
            if Client.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Client(id=obj.id,
                                 dossier=obj.dossier,
                                 nom_prenom=obj.nom_prenom,
                                 adresse=obj.adresse,
                                 commune_id=obj.commune_id,
                                 telephone=obj.telephone
                                 )
                new_obj.save()

    def sync_statuts_document():
        global_objs = GlobalStatutDocument.objects.all()
        for obj in global_objs:
            if StatutDocument.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = StatutDocument(id=obj.id,
                                         statut=obj.statut
                                         )
                new_obj.save()

    def sync_statuts_produit():
        global_objs = GlobalStatutProduit.objects.all()
        for obj in global_objs:
            if StatutProduit.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = StatutProduit(id=obj.id,
                                        statut=obj.statut
                                        )
                new_obj.save()

    def sync_formes_pharmaceutique():
        global_objs = GlobalFormePharmaceutique.objects.all()
        for obj in global_objs:
            if FormePharmaceutique.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = FormePharmaceutique(id=obj.id,
                                              forme=obj.forme
                                              )
                new_obj.save()
                
    def sync_dcis():
        global_objs = GlobalDci.objects.all()
        for obj in global_objs:
            if Dci.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Dci(id=obj.id,
                              code_dci=obj.code_dci,
                              dci=obj.dci,
                              forme_phrmaceutique_id=obj.forme_phrmaceutique_id,
                              dosage=obj.dosage
                              )
                new_obj.save()

    def sync_types_entreposage():
        global_objs = GlobalTypeEntreposage.objects.all()
        for obj in global_objs:
            if TypeEntreposage.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = TypeEntreposage(id=obj.id,
                                          type_entreposage=obj.type_entreposage
                                          )
                new_obj.save()

    def sync_fournisseur():
        global_objs = GlobalFounisseur.objects.all()
        for obj in global_objs:
            if Founisseur.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Founisseur(id=obj.id,
                                     dossier=obj.dossier,
                                     nom=obj.nom
                                     )
                new_obj.save()

    def sync_laboratoire():
        global_objs = GlobalLaboratoire.objects.all()
        for obj in global_objs:
            if Laboratoire.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Laboratoire(id=obj.id,
                                      dossier=obj.dossier,
                                      nom=obj.nom
                                      )
                new_obj.save()

    def sync_produit():
        global_objs = GlobalProduit.objects.all()
        for obj in global_objs:
            if Produit.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = Produit(id=obj.id,
                                  code=obj.code,
                                  produit=obj.produit,
                                  dci_id=obj.dci_id,
                                  conditionnement=obj.conditionnement,
                                  a_rique=obj.a_rique,
                                  psychotrope=obj.psychotrope,
                                  thermosensible=obj.thermosensible,
                                  poids=obj.poids,
                                  volume=obj.volume,
                                  poids_colis=obj.poids_colis,
                                  laboratoire_id=obj.laboratoire_id,
                                  )
                new_obj.save()
    
    def sync_type_mvt_stock():
        global_objs = GlobalTypesMouvementStock.objects.all()
        for obj in global_objs:
            if TypesMouvementStock.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = TypesMouvementStock(id=obj.id,
                                              type=obj.type,
                                              description=obj.description)
                new_obj.save()

    def sync_motifs_inventaire():
        global_objs = GlobalMotifsInventaire.objects.all()
        for obj in global_objs:
            if MotifsInventaire.objects.filter(id=obj.id).exists():
                pass
            else:
                new_obj = MotifsInventaire(id=obj.id,
                                           motif_inventaire=obj.motif_inventaire)
                new_obj.save()
    sync_filiale()
    sync_axe()
    sync_wilaya()
    sync_commune()
    sync_client()
    sync_statuts_document()
    sync_statuts_produit()
    sync_formes_pharmaceutique()
    sync_dcis()
    sync_types_entreposage()
    sync_laboratoire()
    sync_fournisseur()
    sync_produit()
    sync_type_mvt_stock()
    sync_motifs_inventaire()

    return render(request,
                  'rapport.html')
