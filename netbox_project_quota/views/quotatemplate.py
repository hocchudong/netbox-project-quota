from netbox.views import generic
from .. import forms, models, tables
from .. import filtersets


# Quota Template view
class QuotaTemplateView(generic.ObjectView):
    queryset = models.QuotaTemplate.objects.all()

class QuotaTemplateListView(generic.ObjectListView):
    queryset = models.QuotaTemplate.objects.all()
    table = tables.QuotaTemplateTable
    filterset = filtersets.QuotaTemplateFilterSet
    filterset_form = forms.QuotaTemplateFilterForm

class QuotaTemplateEditView(generic.ObjectEditView):
    queryset = models.QuotaTemplate.objects.all()
    form = forms.QuotaTemplateForm

class QuotaTemplateDeleteView(generic.ObjectDeleteView):
    queryset = models.QuotaTemplate.objects.all()

class QuotaTemplateBulkDeleteView(generic.BulkDeleteView):
    queryset = models.QuotaTemplate.objects.all()
    table = tables.QuotaTemplateTable