from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Project, QuotaTemplate
from tenancy.models import Contact
import django_filters


class ProjectFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Project
        fields = ('id', 'name', 'project_id', 'project_owner', 'status', 'quota_template')
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(project_id__icontains=value) |
            Q(project_owner__name__icontains=value) |
            Q(status__icontains=value) |
            Q(quota_template__template_name__icontains=value)
        )
        return queryset.filter(query)


class QuotaTemplateFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = QuotaTemplate
        fields = ('id', 'template_name')
        
    def search(self, queryset, name, value):
        query = Q(
            Q(template_name__icontains=value)
        )
        return queryset.filter(query)