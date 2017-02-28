from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from flux_physique import views as flux_physique_views
from pharmnet_data.views import import_data, import_facture_client
from django.conf import settings
from ajax_select import urls as ajax_select_urls



admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^$', auth_views.login),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', flux_physique_views.logout_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', flux_physique_views.home, name='Home'),
    url(r'^add-transfert/', flux_physique_views.add_transfert, name='add-transfert'),
    url(r'^add-entete-reservation/', flux_physique_views.add_entete_reservation, name='add-entete-reservation'),
    url(r'^add-ligne-reservation/', flux_physique_views.add_ligne_reservation, name='add-ligne-reservation'),
    url(r'^reservation-table/', flux_physique_views.reservation_table, name='reservation-table'),
    url(r'^stock-disponible/', flux_physique_views.stock_disponible, name='stock-disponible'),
    url(r'^stock-disponible-vente/', flux_physique_views.stock_disponible_vente, name='stock-disponible-vente'),
    url(r'^qtt-disponible/', flux_physique_views.qtt_disponible, name='qtt-disponible'),
    url(r'^print_transfert/', flux_physique_views.print_transfert, name='print'),
    url(r'^print_entreposage/', flux_physique_views.print_entreposage, name='print-entreposage'),
    url(r'^validate-transaction-view/', flux_physique_views.validate_transaction_view, name='validate_transaction_view'),
    url(r'^validate-reception-view/', flux_physique_views.validate_receptipon_view, name='validate_reception_view'),
    url(r'^validate-transaction/', flux_physique_views.post_validation, name='validate_transaction'),
    url(r'^transactions-encours/', flux_physique_views.transactions_encours, name='transactions_encours'),
    url(r'^receptions-encours/', flux_physique_views.reception_encours, name='receptions_encours'),
    url(r'^get_employee_name/', flux_physique_views.return_emplyee_by_coderh, name='get_employee_name'),
    url(r'^add-entreposage/', flux_physique_views.add_entreposage, name='add-entreposage'),
    url(r'^add-sortie-colis/', flux_physique_views.add_sortie_en_colis, name='add-sortie-en-colis'),
    url(r'^add-entreposage-reservation/', flux_physique_views.add_entreposage_reservation, name='add-entreposage-reservation'),
    url(r'^entreposage-reservation-table/', flux_physique_views.entreposage_reservation_table, name='entreposage-reservation-table'),
    url(r'^entreposage-add-ligne-reservation/', flux_physique_views.entreposage_add_ligne_reservation,
        name='entreposage-add-ligne-reservation'),
    url(r'^raport-stock/', flux_physique_views.stock_par_magasin, name='raport-stock'),
    url(r'^raport-stock-categorie/', flux_physique_views.stock_par_categorie, name='raport-stock-categorie'),
    url(r'^list-mouvements/', flux_physique_views.list_mouvements, name='list-mouvements'),
    url(r'^details-par-mouvement/', flux_physique_views.details_par_mouvement, name='details-par-mouvement'),
    url(r'^list-achats/', flux_physique_views.list_achats, name='list-achats'),
    url(r'^stock-csv/', flux_physique_views.stock_csv, name='stock-csv'),
    url(r'^produits-par-magasin/', flux_physique_views.produits_par_magasin, name='produits-par-magasin'),
    url(r'^liste-des-emplacements/', flux_physique_views.list_des_emplacement, name='liste-des-emplacements'),
    url(r'^liste-des-produit/', flux_physique_views.list_des_produit, name='liste-des-produit'),
    url(r'^import/', import_data),
    url(r'^import_facture_client/', import_facture_client),
    url(r'^rapport/', flux_physique_views.rapport_efforts),
    )
urlpatterns += staticfiles_urlpatterns()
urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

