from dbfread import DBF
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from flux_physique.models import *
from pharmnet_data.forms import UploadAchatFileForm, UploadFactureFileForm
from refereces.models import *


@login_required(login_url='/login/')
@permission_required('flux_physique.importer_achats', raise_exception=True)
@transaction.atomic
def import_data(request):
    current_exercice = Parametres.objects.get(id=1).exercice
    default_magasin_picking = Parametres.objects.get(id=1).magasin_picking
    default_emplacement_picking = Emplacement.objects.order_by('id').filter(
        magasin=default_magasin_picking).first().emplacement
    default_emplacement_recption = Parametres.objects.get(id=1).emplacement_achat
    username = ' '.join((request.user.first_name, request.user.last_name))
    user_id = request.user.id
    count_laboratoires = 0
    count_fournisseur = 0
    count_entete_achat = 0
    count_formes_pharmaceutiques = 0
    count_dci = 0
    count_produit = 0
    count_lignes_achat = 0
    count_emplacement = 0
    form = UploadAchatFileForm()
    if request.method == 'POST':
        form = UploadAchatFileForm(request.POST, request.FILES)
        if form.is_valid():
            entete_file = request.FILES['entete_achats_file']
            details_file = request.FILES['details_achats_file']

            #  ******************fournisseurs**********************************

            with open('upload.dbf', 'wb+') as destination:
                for chunk in entete_file.chunks():
                    destination.write(chunk)
            db = DBF("upload.dbf", encoding='CP850')
            for data in db.records:
                new_dossier_fournisseur = data['ECFRS']
                new_designation_fournisseur = data['ELFRS']
                new_entete_achat_id = data['ENMVT']
                new_date_mouvement = data['EDMVT']
                new_num_facture = data['ENFACT']
                if not Founisseur.objects.filter(dossier__contains=new_dossier_fournisseur):
                    new_fournisseur = Founisseur(
                        dossier=new_dossier_fournisseur,
                        nom=new_designation_fournisseur
                    )
                    new_fournisseur.save()
                    count_fournisseur += 1
                if not AchatsFournisseur.objects.filter(n_BL__exact=new_entete_achat_id):
                    new_entete_obj = AchatsFournisseur(
                        fournisseur=Founisseur.objects
                        .get(dossier=new_dossier_fournisseur),
                        n_BL=new_entete_achat_id,
                        curr_exercice='2017',
                        date_entree=new_date_mouvement,
                        n_FAC=new_num_facture,
                        statut_doc_id=1,
                        observation='Importation PHARMNET',
                        created_by_id=user_id
                    )
                    new_entete_obj.save()
                    count_entete_achat += 1
            with open('upload.dbf', 'wb+') as destination:
                for chunk in details_file.chunks():
                    destination.write(chunk)
            db = DBF("upload.dbf", encoding=' CP850')
            for data in db.records:
                new_dossier_laboratoire = data['LFRS1']
                new_designation_laboratoire = data['LLIBFRS1']
                new_form_pharmaceutique_str = (data['LFORME']).replace('.', ' ')
                new_code_dci = str(data['LCDCI'])
                new_dci = data['LDCI']
                new_dosage = data['LDOSA']
                new_zone = data['LDEPOT']
                new_emplacement = data['LSDEPOT']
                new_emplacement_zone = new_zone + '.' + new_emplacement
                new_code_produit = data['LCPROD']
                new_produit = data['LCMRC']
                new_entete_achat_id = data['LNMVT']
                new_prix_achat = data['LPVU1']
                new_prix_vente = data['LPVU3']
                new_tva = data['LTVA']
                new_shp = data['LSHP4']
                new_ppa_ht = data['LPVU4A']
                new_n_lot = data['LNLOT']
                new_date_peremption = data['LPEREMP']
                new_colisage = data['LCOLISA']
                new_qtt = data['LQTE']
                new_reference_unique = ''.join((str(current_exercice), str(new_entete_achat_id), str(data['LSUIT'])))

                # ******************Laboratoire**********************************

                if not Laboratoire.objects.filter(dossier__exact=new_dossier_laboratoire):
                    new_fournisseur = Laboratoire(
                        dossier=new_dossier_laboratoire,
                        nom=new_designation_laboratoire
                    )
                    new_fournisseur.save()
                    count_laboratoires += 1

                # ******************formes pharmaceutiques**********************************

                if not FormePharmaceutique.objects.filter(forme__exact=new_form_pharmaceutique_str):
                    new_form_pharmaceutique = FormePharmaceutique(forme=new_form_pharmaceutique_str)
                    new_form_pharmaceutique.save()
                    count_formes_pharmaceutiques += 1

                # ******************DCI**********************************

                if not Dci.objects.filter(code_dci__exact=new_code_dci):
                    if len(new_code_dci) != 0:
                        new_dci_obj = Dci(
                            code_dci=new_code_dci,
                            dci=new_dci,
                            dosage=new_dosage,
                            forme_phrmaceutique=FormePharmaceutique.objects.get(
                                forme=new_form_pharmaceutique_str)
                        )
                        new_dci_obj.save()
                        count_dci += 1
                # *****************Emplacement**********************************

                if not Emplacement.objects.filter(emplacement__exact=new_emplacement_zone):
                    new_emplacement_obj = Emplacement(
                        emplacement=new_emplacement_zone,
                        magasin=default_magasin_picking
                    )
                    new_emplacement_obj.save()
                    count_emplacement += 1

                # *****************Produits**********************************
                if not Produit.objects.filter(code__exact=new_code_produit):
                    if new_emplacement_zone != '.':
                        emplacement_picking = new_emplacement_zone
                    else:

                        emplacement_picking = default_emplacement_picking
                    new_dci_obj = Produit(
                        code=new_code_produit,
                        produit=new_produit,
                        dci=Dci.objects.get(code_dci=new_code_dci),
                        laboratoire=Laboratoire.objects.get(dossier=new_dossier_laboratoire),
                        prelevement=Emplacement.objects.get(emplacement=emplacement_picking)
                    )
                    new_dci_obj.save()
                    count_produit += 1
                # *****************Lignes Achats**********************************
                if not DetailsAchatsFournisseur.objects.filter(
                        ref_unique=new_reference_unique):
                    new_ligne_achat = DetailsAchatsFournisseur(
                        entete=AchatsFournisseur.objects.get(n_BL=new_entete_achat_id),
                        produit=Produit.objects.get(code=new_code_produit),
                        n_lot=new_n_lot,
                        conformite_id=1,
                        emplacement=default_emplacement_recption,
                        prix_achat=new_prix_achat,
                        prix_vente=new_prix_vente,
                        taux_tva=new_tva,
                        shp=new_shp,
                        ppa_ht=new_ppa_ht,
                        date_peremption=new_date_peremption,
                        colisage=new_colisage,
                        qtt=new_qtt,
                        ref_unique=new_reference_unique,
                        created_by_id=user_id
                    )
                    new_ligne_achat.save()
                    count_lignes_achat += 1
            return render(
                request,
                'pharmnet_data/import_list.html',
                {
                    'username': username,
                    'laboratoires': count_laboratoires,
                    'fournisseurs': count_fournisseur,
                    'achats': count_entete_achat,
                    'formes_pharmaceutique': count_formes_pharmaceutiques,
                    'dci': count_dci,
                    'count_produit': count_produit,
                    'count_lignes_achats': count_lignes_achat,
                    'count_emplacement': count_emplacement
                })
        else:
            return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})

    else:
        return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})


def import_facture_client(request):
    default_magasin_picking = Parametres.objects.get(id=1).magasin_picking
    curr_exercice = Parametres.objects.get(id=1).exercice
    default_emplacement_picking = Emplacement.objects.order_by('id').filter(
        magasin=default_magasin_picking).first().emplacement
    username = ' '.join((request.user.first_name, request.user.last_name))
    user_id = request.user.id
    count_villes = 0
    count_wilaya = 0
    count_axe = 0
    count_client = 0

    count_laboratoires = 0
    count_fournisseur = 0
    count_entete_facture = 0
    count_formes_pharmaceutiques = 0
    count_dci = 0
    count_produit = 0
    count_lignes_factures = 0
    count_emplacement = 0
    form = UploadFactureFileForm()
    if request.method == 'POST':
        form = UploadFactureFileForm(request.POST, request.FILES)
        if form.is_valid():
            entete_file = request.FILES['entete_facture_file']
            details_file = request.FILES['details_facture_file']
            #  ******************Entetes**********************************

            with open('upload_factures.dbf', 'wb+') as destination:
                for chunk in entete_file.chunks():
                    destination.write(chunk)
            db = DBF("upload_factures.dbf", encoding='CP850')
            for data in db.records:
                new_commune = data['F_VIL']
                new_code_wilaya = data['F_CWIL']
                new_wilaya = data['F_LWIL']
                new_axe = data['F_LSECT']
                new_dossier_client = data['F_CLIENT']
                new_client = data['F_NOMCLI']
                new_adresse = data['F_ADR1']
                new_num_facture = data['F_NFAC']
                new_date_facture = data['F_DATFAC']
                new_num_BL = data['F_REFORI']
                new_data_BL = data['F_DATORI']
                if not Wilaya.objects.filter(code_wilaya=new_code_wilaya).exists():
                    wilaya = Wilaya(
                        code_wilaya=new_code_wilaya,
                        wilaya=new_wilaya
                    )
                    wilaya.save()
                    count_wilaya += 1
                if not Commune.objects.filter(commune=new_commune).exists():
                    commune = Commune(
                        commune=new_commune,
                        wilaya=Wilaya.objects.get(code_wilaya=new_code_wilaya)
                    )
                    commune.save()
                    count_villes += 1
                if not Axe.objects.filter(axe=new_axe).exists():
                    axe = Axe(
                        axe=new_axe
                    )
                    axe.save()
                    count_axe += 1
                if not Client.objects.filter(dossier=new_dossier_client).exists():
                    client = Client(
                        dossier=new_dossier_client,
                        nom_prenom=new_client,
                        adresse=new_adresse,
                        commune=Commune.objects.get(commune=new_commune),
                        axe=Axe.objects.get(axe=new_axe)
                    )
                    client.save()
                    count_client += 1
                if not FacturesClient.objects.filter(n_facrure=new_num_facture).exists():
                    facture_client = FacturesClient(
                        client=Client.objects.get(dossier=new_dossier_client),
                        n_facrure=new_num_facture,
                        date_facture=new_date_facture,
                        n_commande_original=new_num_BL,
                        date_commande_original=new_data_BL,
                        statut_doc_id=2,
                        created_by_id=user_id,
                        curr_exercice=curr_exercice
                    )
                    facture_client.save()
                    count_entete_facture += 1
            with open('upload_factures.dbf', 'wb+') as destination:
                for chunk in details_file.chunks():
                    destination.write(chunk)
            db = DBF("upload_factures.dbf", encoding='CP850')
            for data in db.records:
                new_n_facture = data['G_NFAC']
                new_code_produit = data['G_CPROD']
                new_produit = data['G_DES0']
                new_prix_achat = data['G_PUNIT']
                new_prix_vente = data['G_DEMI']
                new_taux_tva = data['G_TXTVA']
                new_shp = data['G_SHP4']
                new_ppa_ht = data['G_PVU4HT']
                new_n_lot = data['G_NLOT']
                new_date_peremption = data['G_DATPER']
                new_colisage = data['G_COLIS']
                new_qtt = data['G_QTELIV']
                new_reference_unique = ''.join((str(curr_exercice), str(new_n_facture), str(data['G_SUIT'])))
                if not Produit.objects.filter(code=new_code_produit).exists():
                    emplacement_picking = default_emplacement_picking
                    new_dci_obj = Produit(
                        code=new_code_produit,
                        produit=new_produit,
                        prelevement=Emplacement.objects.get(emplacement=emplacement_picking)
                    )
                    new_dci_obj.save()
                    count_produit += 1
                if not DetailsFacturesClient.objects.filter(ref_unique=new_reference_unique).exists():
                    new_facture_line = DetailsFacturesClient(
                        facture_client=FacturesClient.objects.get(n_facrure=new_num_facture),
                        produit=Produit.objects.get(code=new_code_produit),
                        prix_achat=new_prix_achat,
                        prix_vente=new_prix_vente,
                        taux_tva=new_taux_tva,
                        shp=new_shp,
                        ppa_ht=new_ppa_ht,
                        n_lot=new_n_lot,
                        date_peremption=new_date_peremption,
                        colisage=new_colisage,
                        qtt=new_qtt,
                        created_by_id=user_id,
                        ref_unique=new_reference_unique
                    )
                    new_facture_line.save()
                    count_lignes_factures += 1
            return render(
                request,
                'pharmnet_data/import_factures_client_list.html',
                {
                    'username': username,
                    'count_produit': count_produit,
                    'Factures': count_entete_facture,
                    'Lignes factures': count_lignes_factures,
                    })
        else:
            return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})

    else:
        return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})