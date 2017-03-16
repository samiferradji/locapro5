# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.db import transaction
from flux_physique.models import Transfert, Reservation, DetailsTransfert, EnteteTempo, Stock, HistoriqueDuTravail,\
    Validation, DetailsAchatsFournisseur, AchatsFournisseur, Parametres, TransfertsEntreFiliale, \
    DetailsTransfertEntreFiliale
from refereces.models import Emplacement, StatutDocument, Magasin, Employer



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
                return ['OK',new_transfert.id]
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
                return ['OK',new_transfert.id]

@transaction.atomic
def validate_transaction(type_transaction=None, id_transaction=None, created_by=None,
                         code_RH1=None, code_RH2=None, code_RH3=None):
    if type_transaction =="transfert":
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
        groupe_list = [code_RH1, code_RH2, code_RH3]
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

    if type_transaction =="reception":
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
        groupe_list = [code_RH1, code_RH2, code_RH3]
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
        #'prix_achat',
        #'prix_vente',
        #'taux_tva',
        #'shp',
        #'ppa_ht',
        'n_lot',
        #'date_peremption',
        #'colisage',
        #'poids_boite',
        #'volume_boite',
        #'poids_colis',
        'recu',
        ).annotate(sum_qtt=Sum('qtt'))
    stock_c = stock.filter(sum_qtt=0)
    for obj in stock_c:
        new_obj = Stock.objects.filter(
            conformite_id=obj['conformite'],
            produit_id=obj['produit'],
            #prix_achat=obj['prix_achat'],
            #prix_vente=obj['prix_vente'],
            #taux_tva=obj['taux_tva'],
            #shp=obj['shp'],
            #ppa_ht=obj['ppa_ht'],
            n_lot=obj['n_lot'],
            #date_peremption=obj['date_peremption'],
            #colisage=obj['colisage'],
            #poids_boite=obj['poids_boite'],
            #volume_boite=obj['volume_boite'],
            #poids_colis=obj['poids_colis'],
            recu=obj['recu'],
            )
        new_obj.delete()

    return 'ok'


@transaction.atomic
def ajouter_transfert_entre_filiale(vers_filiale_id, entete_reservation_id, user_id):
    depuis_filiale_id = Parametres.objects.get(id=1).filiale_id
    if depuis_filiale_id == vers_filiale_id :
        return 'Vous ne pouvez pas faire un transfert vers votre filiale'
    else:
        new_transfert = TransfertsEntreFiliale(depuis_filiale_id=depuis_filiale_id,
                                               vers_filiale_id=vers_filiale_id,
                                               statut_doc_id=1,
                                               created_by_id=user_id)
        new_transfert.save()
        for obj in Reservation.objects.filter(id= entete_reservation_id):
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
                created_by_id=user_id
            )
            new_line.save()
            return 'OK'

@transaction.atomic
def confirmer_transfert_entre_filiale(id_transaction, created_by_id, code_RH1, code_RH2, code_RH3):
    details_contenent_type = ContentType.objects.get_for_model(DetailsTransfertEntreFiliale).id
    transfert_contenent_type = ContentType.objects.get_for_model(TransfertsEntreFiliale).id
    transfert_obj = TransfertsEntreFiliale.objects.get(id=id_transaction)
    transfert_obj.statut_doc_id = 2
    transfert_obj.validate_by_id = created_by_id
    transfert_obj.save()
    id_details_transfert = DetailsTransfertEntreFiliale.objects.filter(entete=id_transaction).values_list('id')
    Stock.objects.filter(content_type=details_contenent_type,
                         id_in_content_type__in=id_details_transfert).update(recu=True)
    current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                content_type=transfert_contenent_type)
    current_validation.created_by_id = created_by_id  # initialised with id = admin
    current_validation.save()  # TODO corriger la validation sur transfert et achat , id = admin, then update
    groupe_list = [code_RH1, code_RH2, code_RH3]
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

@transaction.atomic
def expedier_transfert_entre_filiales(id_transaction, created_by_id, code_RH1, code_RH2, code_RH3):
    pass  # il faux créer une table pour les expéditions , puis event --> validation , then update

@transaction.atomic
def reception_transferts_entre_filiales(id_transaction, created_by_id, code_RH1, code_RH2, code_RH3):
    pass  #  lors de la confirmation d'un transfert entre filiale, créer deux validation avec deux motifs
          #  différents: transfert EF et recption TEF