from ajax_select import make_ajax_form
from django.contrib import admin
from flux_physique.models import *


class StockAdmin(admin.ModelAdmin):
    list_display = (
       'id','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','emplacement','conformite', 'qtt','motif','recu'
    )
    list_per_page = 30
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']


@admin.register(DetailsTransfert)
class DetailsTransfertAdmin(admin.ModelAdmin):
    list_display = (
        'id', )
    list_per_page = 30
    #search_fields = ['produit__produit','n_lot','ppa_ht']
    form = make_ajax_form(DetailsTransfert, {
        'produit': 'produits',
        'entete': 'transfers'

        })


class DetailsFacturesClientsAdmin(admin.ModelAdmin):
    list_display = (
        'produit','facture_client','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','qtt'
    )
    list_per_page = 30
    search_fields = ['produit__produit','n_lot','ppa_ht']


class FacturesClientsAdmin(admin.ModelAdmin):
    list_display = ('id','n_facrure','date_facture','client','n_commande_original','statut_doc')
    list_per_page = 30
    search_fields = ['client__nom_prenom','n_facrure','n_commande_original']

class DetailsInventaireAdmin(admin.ModelAdmin):
    list_display = (
        'entete','produit','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','emplacement','conformite', 'qtt'
    )
    list_per_page = 20
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']


class TransfertAdmin(admin.ModelAdmin):
    list_display = ['id','created_date','depuis_magasin','vers_magasin','statut_doc','motif','created_by']
    list_per_page = 30


class AchatsAdmin(admin.ModelAdmin):
    list_display =['id','n_BL','date_entree','n_FAC','fournisseur','observation','statut_doc','created_by','created_date']


class DetailsAchatsAdmin(admin.ModelAdmin):
    list_display = ['id','entete','produit','prix_achat','prix_vente','n_lot','date_peremption','colisage',
        'taux_tva','shp','ppa_ht','emplacement','conformite', 'qtt']
    list_per_page = 20
    search_fields = ['produit__produit', 'n_lot', 'ppa_ht']

admin.site.register(AchatsFournisseur, AchatsAdmin)
admin.site.register(DetailsAchatsFournisseur, DetailsAchatsAdmin)
admin.site.register(CommandesClient)
admin.site.register(DetailsCommandeClient)
admin.site.register(FacturesClient, FacturesClientsAdmin)
admin.site.register(DetailsFacturesClient, DetailsFacturesClientsAdmin)
admin.site.register(Transfert, TransfertAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Reservation)
admin.site.register(Inventaire)
admin.site.register(DetailsInventaire, DetailsInventaireAdmin)
admin.site.register(MotifsInventaire)
admin.site.register(Validation)
admin.site.register(HistoriqueDuTravail)
admin.site.register(Parametres)