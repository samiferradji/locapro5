from ajax_select import make_ajax_form
from django.contrib import admin
from flux_physique.models import *


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_select_related = ('produit', 'emplacement', 'conformite')
    list_display = (
        'id', 'produit','prix_achat', 'prix_vente', 'n_lot', 'date_peremption','colisage',
        'taux_tva', 'shp','ppa_ht', 'emplacement', 'conformite', 'qtt', 'motif', 'recu'
    )
    list_per_page = 30
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']

@admin.register(DetailsTransfert)
class DetailsTransfertAdmin(admin.ModelAdmin):
    list_select_related = ('produit', 'depuis_emplacement', 'vers_emplacement', 'conformite','entete', 'created_by')
    list_per_page = 30
    list_display = ['id', 'entete', 'produit','prix_achat', 'prix_vente', 'n_lot', 'date_peremption','colisage',
                    'taux_tva', 'shp','ppa_ht', 'depuis_emplacement', 'vers_emplacement', 'conformite', 'qtt'
                    ]
    form = make_ajax_form(DetailsTransfert, {
        'produit': 'produits',
        'depuis_emplacement': 'emplacements',
        'vers_emplacement': 'emplacements',
        'entete': 'transferts'
    })


@admin.register(DetailsFacturesClient)
class DetailsFacturesClientsAdmin(admin.ModelAdmin):
    list_display = (
        'produit','facture_client','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','qtt'
    )
    list_per_page = 30
    search_fields = ['produit__produit','n_lot','ppa_ht']


@admin.register(FacturesClient)
class FacturesClientsAdmin(admin.ModelAdmin):
    list_display = ('id','n_facrure','date_facture','client','n_commande_original','statut_doc')
    list_per_page = 30
    search_fields = ['client__nom_prenom','n_facrure','n_commande_original']


@admin.register(DetailsInventaire)
class DetailsInventaireAdmin(admin.ModelAdmin):
    list_select_related = ('produit', 'emplacement', 'conformite', 'entete', 'created_by')
    list_display = (
        'entete','produit','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','emplacement','conformite', 'qtt'
    )
    list_per_page = 20
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']
    form = make_ajax_form(DetailsInventaire, {
        'produit': 'produits',
        'emplacement': 'emplacements',
        })


@admin.register(Transfert)
class TransfertAdmin(admin.ModelAdmin):
    list_display = ['id','created_date','depuis_magasin','vers_magasin','statut_doc','motif','created_by']
    list_per_page = 30


@admin.register(AchatsFournisseur)
class AchatsAdmin(admin.ModelAdmin):
    list_display =['id','n_BL','date_entree','n_FAC','fournisseur','observation','statut_doc','created_by','created_date']

@admin.register(DetailsAchatsFournisseur)
class DetailsAchatsAdmin(admin.ModelAdmin):
    list_display = ['id','entete','produit','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','emplacement','conformite', 'qtt']
    list_per_page = 20
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']


admin.site.register(CommandesClient)
admin.site.register(DetailsCommandeClient)
admin.site.register(Reservation)
admin.site.register(Inventaire)
admin.site.register(MotifsInventaire)
admin.site.register(Validation)
admin.site.register(HistoriqueDuTravail)
admin.site.register(Parametres)
admin.site.register(ExpeditionTransfertsEntreFiliale)
admin.site.register(DetailsExpeditionTransfertsEntreFiliale)

@admin.register(TransfertsEntreFiliale)
class TransfertEntreFilialeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_date', 'depuis_filiale', 'vers_filiale', 'statut_doc', 'created_by']
    list_per_page = 30
    list_filter = ['depuis_filiale', 'vers_filiale', 'statut_doc']
    search_fields = ['id']


@admin.register(DetailsTransfertEntreFiliale)
class DetailsTransfertEntreFilialeAdmin(admin.ModelAdmin):
    list_select_related = ('produit', 'conformite','entete', 'created_by')
    list_per_page = 30
    list_display = ['id', 'entete', 'produit','prix_achat', 'prix_vente', 'n_lot', 'date_peremption','colisage',
                    'taux_tva', 'shp', 'ppa_ht', 'conformite', 'qtt'
                    ]
    search_fields = ['entete', 'produit__produit']
    form = make_ajax_form(DetailsTransfertEntreFiliale, {
        'produit': 'produits',
        'entete': 'transferts_entre_filiale'
    })