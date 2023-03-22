from .models import Project, QuotaTemplate, ProjectStatusChoices
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import ConfirmationForm, BootstrapMixin, TagFilterField, MultipleChoiceField
from django import forms
from dcim.models import Device, DeviceRole, Platform, Rack, Region, Site, SiteGroup
from ipam.models import IPAddress
from tenancy.models import Contact
from virtualization.models import ClusterGroup, Cluster, VirtualMachine


class ProjectForm(NetBoxModelForm):
    project_owner = DynamicModelChoiceField(
        queryset=Contact.objects.all()
    )
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    fieldsets = (
        (
            'General', 
            (
                'name', 
                'project_id', 
                'project_owner', 
                'status', 
                'quota_template',
                'description',
                'tags'
            )
        ),
    )
    class Meta:
        model = Project
        fields = ('name', 'project_id', 'project_owner', 'status', 'quota_template', 'description', 'comments', 'tags')


class ProjectFilterForm(NetBoxModelFilterSetForm):
    model = Project
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Project', (
            'project_owner_id', 'project_id', 'status', 'quota_template_id'
        )),
        ('Attributes', (
            'contact_id', 'virtualmachine_id', 'ipaddress_id', 'devices_id'
        ))
    )
    project_owner_id = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label='Contact Point'
    )

    project_id = forms.CharField(
        required=False,
    )
    status = MultipleChoiceField(
        choices=ProjectStatusChoices,
        required=False,
    )
    quota_template_id = DynamicModelChoiceField(
        queryset=QuotaTemplate.objects.all(),
        required=False,
        label='Quota Template'
    )
    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label='User'
    )
    virtualmachine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label='VM'
    )
    ipaddress_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label='IP Address'
    )
    devices_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label='Device'
    )
    tag = TagFilterField(model)


class QuotaTemplateForm(NetBoxModelForm):
    template_name = forms.CharField(
        label='Name',
    )
    instances_quota = forms.IntegerField(
        label='VM Quota',
        required=False
    )

    vcpus_quota = forms.IntegerField(
        label='VCPUs Quota',
        required=False
    )

    ram_quota = forms.IntegerField(
        label='RAM Quota (MB)',
        required=False
    )

    ipaddr_quota = forms.IntegerField(
        label='IP Quota',
        required=False
    )

    device_quota = forms.IntegerField(
        label='Device Quota',
        required=False
    )
    
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    fieldsets = (
        (
            'General', 
            (
                'template_name', 
                'instances_quota', 
                'vcpus_quota', 
                'ram_quota', 
                'ipaddr_quota', 
                'device_quota',
                'description',
                'tags'
            )
        ),
    )
    class Meta:
        model = QuotaTemplate
        fields = ('template_name', 'instances_quota', 'vcpus_quota', 'ram_quota', 'ipaddr_quota', 'device_quota', 'description', 'comments', 'tags')


class QuotaTemplateFilterForm(NetBoxModelFilterSetForm):
    model = QuotaTemplate
    template_name = forms.CharField(
        required=False
    )
    tag = TagFilterField(model)

###### Project Device ######

### Device ADD
class ProjectAddDevicesForm(BootstrapMixin, forms.Form):
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        null_option='None'
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        null_option='None'
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region',
            'group_id': '$site_group',
        }
    )
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site'
        }
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        query_params={
            'site_id': '$site',
            'rack_id': '$rack',
        }
    )

    class Meta:
        fields = [
            'region', 'site', 'rack', 'devices',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['devices'].choices = []

### Device Remove

class ProjectRemoveDevicesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


###### Project IPAddress ######

### IP ADD
class ProjectAddIPAddressForm(BootstrapMixin, forms.Form):
    ipaddress = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
    )
    class Meta:
        fields = [
            'ipaddress'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['ipaddress'].choices = []


### IP Remove

class ProjectRemoveIPsForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        widget=forms.MultipleHiddenInput()
    )

###### Project Instance ######

### VM ADD
class ProjectAddInstanceForm(BootstrapMixin, forms.Form):
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all()
    )
    virtualmachine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        query_params={
            "vm_role": "True",
            'cluster_id': '$cluster'
        }
    )
    class Meta:
        fields = [
            'cluster', 'virtualmachine'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['virtualmachine'].choices = []

### VM Remove
class ProjectRemoveVMsForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class ProjectAddContactForm(BootstrapMixin, forms.Form):
    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
    )
    class Meta:
        fields = [
            'contact'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['contact'].choices = []


class ProjectContactRemoveForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.MultipleHiddenInput()
    )