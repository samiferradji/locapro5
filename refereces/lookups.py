from ajax_select import register, LookupChannel
from .models import Emplacement, Dci, Client, Commune, Employer, Produit
from flux_physique.models import Transfert


@register('emplacements')
class EmplacementLookup(LookupChannel):

    model = Emplacement

    def get_query(self, q, request):
        return self.model.objects.filter(emplacement__icontains=q).order_by('emplacement')[:25]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.emplacement

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.emplacement


@register('dcis')
class DciLookup(LookupChannel):

    model = Dci

    def get_query(self, q, request):
        return self.model.objects.filter(dci__icontains=q).order_by('dci')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % (" ".join((obj.code_dci, obj.dci, str(obj.forme_phrmaceutique))))


@register('clients')
class ClientLookup(LookupChannel):

    model = Client

    def get_query(self, q, request):
        return self.model.objects.filter(client__icontains=q).order_by('client')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.client


@register('communes')
class CommuneLookup(LookupChannel):

    model = Commune

    def get_query(self, q, request):
        return self.model.objects.filter(commune__icontains=q).order_by('commune')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.commune


@register('employees')
class EmployeeLookup(LookupChannel):

    model = Employer

    def get_query(self, q, request):
        return self.model.objects.filter(nom__icontains=q).order_by('commune')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.nom


@register('produits')
class ProduitLookup(LookupChannel):

    model = Produit

    def get_query(self, q, request):
        return self.model.objects.filter(produit__icontains=q).order_by('produit')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.produit


@register('transfers')
class TransfertLookup(LookupChannel):

    model = Transfert

    def get_query(self, q, request):
        return self.model.objects.filter(id__icontains=q).order_by('id')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.id
