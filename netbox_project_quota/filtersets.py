from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Project, QuotaTemplate
from tenancy.models import Contact
from dcim.models import Device
from ipam.models import IPAddress
from tenancy.models import Contact
from virtualization.models import VirtualMachine
import django_filters


class ProjectFilterSet(NetBoxModelFilterSet):
    project_owner_id = django_filters.ModelMultipleChoiceFilter(
        field_name='project_owner',
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )

    quota_template_id = django_filters.ModelMultipleChoiceFilter(
        field_name='quota_template',
        queryset=QuotaTemplate.objects.all(),
        label='Quota Template (ID)',
    )

    contact_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all(),
        label='User (ID)',
    )

    virtualmachine_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtualmachine',
        queryset=VirtualMachine.objects.all(),
        label='VM (ID)',
    )

    ipaddress_id = django_filters.ModelMultipleChoiceFilter(
        field_name='ipaddress',
        queryset=IPAddress.objects.all(),
        label='IP Address (ID)',
    )

    devices_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'project_id',
            'project_owner',
            'status',
            'quota_template',
            'contact',
            'virtualmachine',
            'devices',
            'ipaddress'
        )

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