# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction
from flux_physique.models import Transfert, Reservation, DetailsTransfert, EnteteTempo, Stock, HistoriqueDuTravail, \
    Validation, DetailsAchatsFournisseur, AchatsFournisseur, Parametres, TransfertsEntreFiliale, \
    DetailsTransfertEntreFiliale, ExpeditionTransfertsEntreFiliale, MotifsInventaire

from refereces.models import *



@transaction.atomic
def commit_transaction(transaction_type=None, user=None, depuis_magasin=None, vers_magasin=None,
                       entete_tempo=None, motif=None):
    if transaction_type == 'save_transfert':
        user = user
        entete_tempo = entete_tempo
        depuis_magasin = depuis_magasin
        vers_magasin = vers_magasin
        default_emplacement = Emplacement.objects.filter(magasin_id=vers_magasin).order_by('id').first()
        default_statut = StatutDocument.objects.order_by('id').first()
        reservation_details = Reservation.objects.filter(entete_tempo=entete_tempo).all()
        if reservation_details.exists():
            picking_magasin_id = Parametres.objects.get(id=1).magasin_picking_id
            if vers_magasin == picking_magasin_id and motif == 1:  # TODO Standardissr cette clause avec paramettres
                motif = 5
            new_transfert = Transfert(
                created_by=user,
                depuis_magasin=Magasin.objects.get(id=depuis_magasin),
                vers_magasin=Magasin.objects.get(id=vers_magasin),
                statut_doc=default_statut,
                motif_id=motif
            )
            new_transfert.save()
            for item in reservation_details:
                if vers_magasin == Parametres.objects.get(id=1).magasin_picking_id:
                    new_transfert_details = DetailsTransfert(
                        created_by=user,
                        entete=new_transfert,
                        id_in_content_type=item.id_stock.id_in_content_type,
                        content_type=item.id_stock.content_type,
                        conformite=item.id_stock.conformite,
                        depuis_emplacement=item.id_stock.emplacement,
                        vers_emplacement=item.id_stock.produit.prelevement,
                        produit=item.id_stock.produit,
                        prix_achat=item.id_stock.prix_achat,
                        prix_vente=item.id_stock.prix_vente,
                        taux_tva=item.id_stock.taux_tva,
                        shp=item.id_stock.shp,
                        ppa_ht=item.id_stock.ppa_ht,
                        n_lot=item.id_stock.n_lot,
                        date_peremption=item.id_stock.date_peremption,
                        colisage=item.id_stock.colisage,
                        poids_boite=item.id_stock.poids_boite,
                        volume_boite=item.id_stock.volume_boite,
                        poids_colis=item.id_stock.poids_colis,
                        qtt=item.qtt,
                    )
                    new_transfert_details.save()
                else:
                    new_transfert_details = DetailsTransfert(
                        created_by=user,
                        entete=new_transfert,
                        id_in_content_type=item.id_stock.id_in_content_type,
                        content_type=item.id_stock.content_type,
                        conformite=item.id_stock.conformite,
                        depuis_emplacement=item.id_stock.emplacement,
                        vers_emplacement=default_emplacement,
                        produit=item.id_stock.produit,
                        prix_achat=item.id_stock.prix_achat,
                        prix_vente=item.id_stock.prix_vente,
                        taux_tva=item.id_stock.taux_tva,
                        shp=item.id_stock.shp,
                        ppa_ht=item.id_stock.ppa_ht,
                        n_lot=item.id_stock.n_lot,
                        date_peremption=item.id_stock.date_peremption,
                        colisage=item.id_stock.colisage,
                        poids_boite=item.id_stock.poids_boite,
                        volume_boite=item.id_stock.volume_boite,
                        poids_colis=item.id_stock.poids_colis,
                        qtt=item.qtt,
                    )
                    new_transfert_details.save()
                entete_tempo_obj = EnteteTempo.objects.filter(id=entete_tempo)
                entete_tempo_obj.delete()
            return ['OK', new_transfert.id]
    if transaction_type == 'save_entreposage':
        user = user
        entete_tempo = entete_tempo
        depuis_magasin = depuis_magasin
        vers_magasin = vers_magasin
        default_statut = StatutDocument.objects.order_by('id').first()
        reservation_details = Reservation.objects.filter(entete_tempo=entete_tempo).all()
        if reservation_details:
            new_transfert = Transfert(
                created_by=user,
                depuis_magasin=Magasin.objects.get(id=depuis_magasin),
                vers_magasin=Magasin.objects.get(id=vers_magasin),
                statut_doc=default_statut,
                motif_id=motif
            )
            new_transfert.save()
            for item in reservation_details:
                new_transfert_details = DetailsTransfert(
                    created_by=user,
                    entete=new_transfert,
                    id_in_content_type=item.id_stock.id_in_content_type,
                    content_type=item.id_stock.content_type,
                    conformite=item.id_stock.conformite,
                    depuis_emplacement=item.id_stock.emplacement,
                    vers_emplacement=item.new_emplacement,
                    produit=item.id_stock.produit,
                    prix_achat=item.id_stock.prix_achat,
                    prix_vente=item.id_stock.prix_vente,
                    taux_tva=item.id_stock.taux_tva,
                    shp=item.id_stock.shp,
                    ppa_ht=item.id_stock.ppa_ht,
                    n_lot=item.id_stock.n_lot,
                    date_peremption=item.id_stock.date_peremption,
                    colisage=item.id_stock.colisage,
                    poids_boite=item.id_stock.poids_boite,
                    volume_boite=item.id_stock.volume_boite,
                    poids_colis=item.id_stock.poids_colis,
                    qtt=item.qtt,
                )
                new_transfert_details.save()
                entete_tempo_obj = EnteteTempo.objects.filter(id=entete_tempo)
                entete_tempo_obj.delete()
            return ['OK', new_transfert.id]


@transaction.atomic
def validate_transaction(type_transaction=None, id_transaction=None, created_by=None,
                         code_rh1=None, code_rh2=None, code_rh3=None):
    if type_transaction == "transfert":
        details_contenent_type = ContentType.objects.get_for_model(DetailsTransfert).id
        transfert_contenent_type = ContentType.objects.get_for_model(Transfert).id
        transfert_obj = Transfert.objects.get(id=id_transaction)
        transfert_obj.statut_doc_id = 2
        transfert_obj.validate_by_id = created_by
        transfert_obj.save()
        id_details_transfert = DetailsTransfert.objects.filter(entete=id_transaction).values_list('id')
        Stock.objects.filter(content_type=details_contenent_type,
                             id_in_content_type__in=id_details_transfert).update(recu=True)
        current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                    content_type=transfert_contenent_type)
        groupe_list = [code_rh1, code_rh2, code_rh3]
        groupe_list = list(filter(None, groupe_list))
        groupe_count = len(groupe_list)
        for item in groupe_list:
            employee = Employer.objects.get(code_RH=item)
            new_execution = HistoriqueDuTravail(
                employer=employee,
                groupe=groupe_count,
                id_validation=current_validation
            )
            new_execution.save()

        return 'OK'

    if type_transaction == "reception":
        details_contenent_type = ContentType.objects.get_for_model(DetailsAchatsFournisseur).id
        reception_contenent_type = ContentType.objects.get_for_model(AchatsFournisseur).id
        reception_obj = AchatsFournisseur.objects.get(n_BL=id_transaction)
        reception_obj.statut_doc_id = 2
        reception_obj.validate_by_id = created_by
        reception_obj.save()
        id_details_reception = DetailsAchatsFournisseur.objects.filter(entete=reception_obj.id).values_list('id')
        Stock.objects.filter(content_type=details_contenent_type,
                             id_in_content_type__in=id_details_reception).update(recu=True)
        current_validation = Validation.objects.get(id_in_content_type=reception_obj.id,
                                                    content_type=reception_contenent_type)
        groupe_list = [code_rh1, code_rh2, code_rh3]
        groupe_list = list(filter(None, groupe_list))
        groupe_count = len(groupe_list)
        for item in groupe_list:
            employee = Employer.objects.get(code_RH=item)
            new_execution = HistoriqueDuTravail(
                employer=employee,
                groupe=groupe_count,
                id_validation=current_validation
            )
            new_execution.save()

        return 'OK'
    else:
        return 'PAS OK'


@transaction.atomic
def compresser_stock():
    stock = Stock.objects.all().values(
        'conformite',
        'emplacement',
        'produit',
        'prix_achat',
        'prix_vente',
        'taux_tva',
        'shp',
        'ppa_ht',
        'n_lot',
        'date_peremption',
        'colisage',
        'poids_boite',
        'volume_boite',
        'poids_colis',
        'recu',
    ).annotate(sum_qtt=Sum('qtt'))
    stock = stock.exclude(sum_qtt=0)
    len_stock = len(stock)
    data_to_delete = Stock.objects.all()
    data_to_delete.delete()
    for obj in stock:
        new_obj = Stock(
            id_in_content_type=1,
            content_type=1000,
            conformite_id=obj['conformite'],
            emplacement_id=obj['emplacement'],
            produit_id=obj['produit'],
            prix_achat=obj['prix_achat'],
            prix_vente=obj['prix_vente'],
            taux_tva=obj['taux_tva'],
            shp=obj['shp'],
            ppa_ht=obj['ppa_ht'],
            n_lot=obj['n_lot'],
            date_peremption=obj['date_peremption'],
            colisage=obj['colisage'],
            poids_boite=obj['poids_boite'],
            volume_boite=obj['volume_boite'],
            poids_colis=obj['poids_colis'],
            qtt=obj['sum_qtt'],
            motif='archivage',
            recu=obj['recu'],
            created_by_id=1
        )
        new_obj.save()

    return 'ok'


@transaction.atomic
def compresser_stock2():
    stock = Stock.objects.all().values(
        'conformite',
        'produit',
        # 'prix_achat',
        # 'prix_vente',
        # 'taux_tva',
        # 'shp',
        # 'ppa_ht',
        'n_lot',
        # 'date_peremption',
        # 'colisage',
        # 'poids_boite',
        # 'volume_boite',
        # 'poids_colis',
        'recu',
    ).annotate(sum_qtt=Sum('qtt'))
    stock_c = stock.filter(sum_qtt=0)
    for obj in stock_c:
        new_obj = Stock.objects.filter(
            conformite_id=obj['conformite'],
            produit_id=obj['produit'],
            # prix_achat=obj['prix_achat'],
            # prix_vente=obj['prix_vente'],
            # taux_tva=obj['taux_tva'],
            # shp=obj['shp'],
            # ppa_ht=obj['ppa_ht'],
            n_lot=obj['n_lot'],
            # date_peremption=obj['date_peremption'],
            # colisage=obj['colisage'],
            # poids_boite=obj['poids_boite'],
            # volume_boite=obj['volume_boite'],
            # poids_colis=obj['poids_colis'],
            recu=obj['recu'],
        )
        new_obj.delete()

    return 'ok'


def synch_data():
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

    def sync_transfert_entre_filiale():
        global_objs = GlobalTransfertsEntreFiliale.objects.all()
        for obj in global_objs:
            if TransfertsEntreFiliale.objects.filter(id=obj.id).exists():
                current_transfert = TransfertsEntreFiliale.objects.get(id=obj.id)
                if current_transfert.statut_doc_id == obj.statut_doc_id:
                    pass
                else:
                    current_transfert.statut_doc_id = obj.statut_doc_id
                    current_transfert.save()
            else:
                new_obj = TransfertsEntreFiliale(
                    id=obj.id,
                    depuis_filiale_id=obj.depuis_filiale_id,
                    vers_filiale_id=obj.vers_filiale_id,
                    statut_doc_id=obj.statut_doc_id,
                    created_by_id=1,
                    nombre_colis=obj.nombre_colis,
                    nombre_colis_frigo=obj.nombre_colis_frigo
                )
                new_obj.save()
                details_obj = GlobalDetailsTransfertEntreFiliale.objects.filter(entete_id=obj.id)
                for line in details_obj:
                    new_line = DetailsTransfertEntreFiliale(
                        id=line.id,
                        entete_id=obj.id,
                        conformite_id=line.conformite_id,
                        produit_id=line.produit_id,
                        prix_achat=line.prix_achat,
                        prix_vente=line.prix_vente,
                        taux_tva=line.taux_tva,
                        shp=line.shp,
                        ppa_ht=line.ppa_ht,
                        n_lot=line.n_lot,
                        date_peremption=line.date_peremption,
                        colisage=line.colisage,
                        poids_boite=line.poids_boite,
                        volume_boite=line.volume_boite,
                        poids_colis=line.poids_colis,
                        qtt=line.qtt,
                        created_by_id=1,
                        depuis_emplacement_id=Parametres.objects.get(id=1).emplacement_achat_id,
                        vers_emplacement_id=Parametres.objects.get(id=1).emplacement_achat_id
                    )
                    new_line.save()

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
    sync_transfert_entre_filiale()

    return 'OK'


def ajouter_transfert_entre_filiale(vers_filiale_id, entete_reservation_id, user_id):
    depuis_filiale_id = Parametres.objects.get(id=1).filiale.id
    if depuis_filiale_id == vers_filiale_id:
        return 'Vous ne pouvez pas faire un transfert vers votre filiale'
    else:
        new_transfert = TransfertsEntreFiliale(depuis_filiale_id=depuis_filiale_id,
                                               vers_filiale_id=vers_filiale_id,
                                               statut_doc_id=1,
                                               created_by_id=user_id)
        new_transfert.save()
        default_emplacement = Parametres.objects.get(id=1).emplacement_expedition_transfert_entre_filiale
        for obj in Reservation.objects.filter(entete_tempo=entete_reservation_id).all():
            new_line = DetailsTransfertEntreFiliale(
                entete_id=new_transfert.id,
                conformite_id=obj.id_stock.conformite_id,
                produit_id=obj.id_stock.produit_id,
                prix_achat=obj.id_stock.prix_achat,
                prix_vente=obj.id_stock.prix_vente,
                taux_tva=obj.id_stock.taux_tva,
                shp=obj.id_stock.shp,
                ppa_ht=obj.id_stock.ppa_ht,
                n_lot=obj.id_stock.n_lot,
                date_peremption=obj.id_stock.date_peremption,
                colisage=obj.id_stock.colisage,
                poids_boite=obj.id_stock.poids_boite,
                volume_boite=obj.id_stock.volume_boite,
                poids_colis=obj.id_stock.poids_colis,
                qtt=obj.qtt,
                created_by_id=user_id,
                depuis_emplacement=obj.id_stock.emplacement,
                vers_emplacement=default_emplacement,
                created_date=timezone.now(),
                modified_date=timezone.now()
                )
            new_line.save()
        return ['OK', new_transfert.id]



#@transaction.atomic
def confirmer_transfert_entre_filiale(id_transaction, created_by_id, code_rh1, code_rh2, code_rh3, nombre_colis,
                                      nombre_colis_frigo):
    try:

        details_contenent_type = ContentType.objects.get_for_model(DetailsTransfertEntreFiliale).id
        transfert_contenent_type = ContentType.objects.get_for_model(TransfertsEntreFiliale).id
        transfert_obj = TransfertsEntreFiliale.objects.get(id=id_transaction)
        if transfert_obj.statut_doc_id == 2:
            return 'Ce bon est déja validé'
        elif transfert_obj.depuis_filiale != Parametres.objects.get(id=1).filiale:
            return 'Vous ne pouvez pas valider ce Bon'
        else:
            transfert_obj.statut_doc_id = 2
            transfert_obj.nombre_colis = nombre_colis
            transfert_obj.nombre_colis_frigo = nombre_colis_frigo
            transfert_obj.save()
            id_details_transfert = DetailsTransfertEntreFiliale.objects.filter(entete=id_transaction).values_list('id')
            if id_details_transfert.exists():
               Stock.objects.filter(content_type=details_contenent_type,
                                    id_in_content_type__in=id_details_transfert).update(recu=True)
            current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                    content_type=transfert_contenent_type)
            current_validation.created_by_id = created_by_id  # initialised with id = admin
            current_validation.save()  # TODO corriger la validation sur transfert et achat , id = admin, then update
            groupe_list = [code_rh1, code_rh2, code_rh3]
            groupe_list = list(filter(None, groupe_list))
            groupe_count = len(groupe_list)
            for item in groupe_list:
                employee = Employer.objects.get(code_RH=item).id
                HistoriqueDuTravail(
                   employer_id=employee,
                   groupe=groupe_count,
                   id_validation=current_validation).save()
            return 'OK'
    except Exception as e:
        return e

@transaction.atomic
def expedition_transferts_entre_filiales(id_transaction, created_by_id, code_rh1, code_rh2, code_rh3,
                                         livreur, fourgon):
    try :
        current_contenent_type = ContentType.objects.get_for_model(ExpeditionTransfertsEntreFiliale).id
        transfert_obj = TransfertsEntreFiliale.objects.get(id=id_transaction)
        transfert_obj.statut_doc_id = 3
        transfert_obj.save()
        current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                    content_type=current_contenent_type)
        current_validation.created_by_id = created_by_id  # initialised with id = admin
        current_validation.save()
        current_expedition = ExpeditionTransfertsEntreFiliale.objects.get(id=id_transaction)
        current_expedition.fourgon = fourgon
        current_expedition.livreur = livreur
        current_expedition.save()
        groupe_list = [code_rh1, code_rh2, code_rh3]
        groupe_list = list(filter(None, groupe_list))
        groupe_count = len(groupe_list)
        for item in groupe_list:
            employee = Employer.objects.get(code_RH=item)
            new_execution = HistoriqueDuTravail(
                employer=employee,
                groupe=groupe_count,
                id_validation=current_validation
            )
            new_execution.save()
        return 'OK'
    except Exception as e:
        return e

@transaction.atomic
def reception_transferts_entre_filiales(id_transaction, created_by_id, code_rh1, code_rh2, code_rh3):
    try:
        transfert_contenent_type = ContentType.objects.get_for_model(TransfertsEntreFiliale).id
        transfert_obj = TransfertsEntreFiliale.objects.get(id=id_transaction)
        if transfert_obj.statut_doc_id == 4:
            return 'Ce bon est déja validé'
        elif transfert_obj.vers_filiale != Parametres.objects.get(id=1).filiale:
            return 'Vous ne pouvez pas valider ce Bon'
        else:
            transfert_obj.statut_doc_id = 4
            transfert_obj.save()
            current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                        content_type=transfert_contenent_type)
            current_validation.created_by_id = created_by_id  # initialised with id = admin
            current_validation.save()
            groupe_list = [code_rh1, code_rh2, code_rh3]
            groupe_list = list(filter(None, groupe_list))
            groupe_count = len(groupe_list)
            for item in groupe_list:
                employee = Employer.objects.get(code_RH=item)
                new_execution = HistoriqueDuTravail(
                    employer=employee,
                    groupe=groupe_count,
                    id_validation=current_validation
                )
                new_execution.save()
            return 'OK'
    except Exception as e:
        return e


