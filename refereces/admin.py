from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from refereces.models import *
from ajax_select import make_ajax_form


admin.site.site_title = 'LOCAPRO 5'
admin.site.site_header = 'LOCAPRO 5'
admin.site.register(Axe)
admin.site.register(Wilaya)
admin.site.register(StatutDocument)
admin.site.register(StatutProduit)
admin.site.register(Magasin)
admin.site.register(Founisseur)
admin.site.register(Laboratoire)
admin.site.register(TypesMouvementStock)
admin.site.register(Employer)
admin.site.register(TypeEntreposage)


class DepuisMagasinsInline(admin.TabularInline):
    model = DepuisMagasinsAutorise
    extra = 1


class VersMagasinsInline(admin.TabularInline):
    model = VersMagasinsAutorise
    extra = 1


class StatutsInline(admin.TabularInline):
    model = StatutsAutorise
    extra = 1


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(AuthUserAdmin):
    list_display = ('get_code_rh', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('userprofile',)

    def get_code_rh(self, instance):
        return instance.userprofile.code_employee
    get_code_rh.short_description = 'Code Employé'

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline, DepuisMagasinsInline, VersMagasinsInline, StatutsInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Produit)
class ProduitModelAdmin(admin.ModelAdmin):

    form = make_ajax_form(Produit, {
        'prelevement': 'emplacements',
        'dci': 'dcis'
    })
    list_display = ('code', 'produit', 'laboratoire', 'thermosensible', 'psychotrope',
                    'prelevement', 'seuil_min', 'seuil_max')
    list_per_page = 30
    search_fields = ['code', 'produit']


@admin.register(Client)
class ClientModelAdmin(AjaxSelectAdmin):

    form = make_ajax_form(Client, {
        'commune': 'communes',
        })
    list_display = ('dossier', 'nom_prenom', 'commune', 'axe', 'telephone')
    list_per_page = 30
    search_fields = ['dossier', 'nom_prenom']


@admin.register(Commune)
class CommuneModelAdmin(admin.ModelAdmin):

    list_display = ('code_commune', 'commune', 'wilaya')
    list_per_page = 30
    search_fields = ['code_commune', 'commune']


@admin.register(Dci)
class DciModelAdmin(AjaxSelectAdmin):

    list_display = ('code_dci', 'dci', 'forme_phrmaceutique', 'dosage')
    list_per_page = 30
    search_fields = ['code_dci', 'dci']


@admin.register(Emplacement)
class EmplacementModelAdmin(AjaxSelectAdmin):

    list_display = ('emplacement', 'magasin', 'type_entreposage', 'poids', 'volume',)
    list_per_page = 30
    search_fields = ['emplacement']
