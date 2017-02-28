from ajax_select import register, LookupChannel
from .models import Emplacement, Dci, Client, Commune, Employer


@register('emplacements')
class TagsLookup(LookupChannel):

    model = Emplacement

    def get_query(self, q, request):
        return self.model.objects.filter(emplacement__icontains=q).order_by('emplacement')[:25]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.emplacement

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.emplacement


@register('dcis')
class TagsLookup(LookupChannel):

    model = Dci

    def get_query(self, q, request):
        return self.model.objects.filter(dci__icontains=q).order_by('dci')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % (" ".join((obj.code_dci, obj.dci, str(obj.forme_phrmaceutique))))


@register('clients')
class TagsLookup(LookupChannel):

    model = Dci

    def get_query(self, q, request):
        return self.model.objects.filter(client__icontains=q).order_by('client')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.client


@register('communes')
class TagsLookup(LookupChannel):

    model = Commune

    def get_query(self, q, request):
        return self.model.objects.filter(commune__icontains=q).order_by('commune')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.commune


@register('employees')
class TagsLookup(LookupChannel):

    model = Commune

    def get_query(self, q, request):
        return self.model.objects.filter(nom__icontains=q).order_by('commune')[:25]

    def format_match(self, obj):
        return u"<span class='tag'>%s</span>" % obj.nom