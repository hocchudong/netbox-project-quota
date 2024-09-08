from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Project, QuotaTemplate


class NestedProjectSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_project_quota-api:project-detail'
    )
    device_count = serializers.IntegerField(read_only=True)
    ip_count = serializers.IntegerField(read_only=True)
    vm_count = serializers.IntegerField(read_only=True)
    user_count = serializers.IntegerField(read_only=True)
    ram_quota_used = serializers.CharField(read_only=True)
    cpu_quota_used = serializers.CharField(read_only=True)
    disk_quota_used = serializers.CharField(read_only=True)
    device_quota_used = serializers.CharField(read_only=True)
    vm_quota_used = serializers.CharField(read_only=True)
    ip_quota_used = serializers.CharField(read_only=True)
    class Meta:
        model = Project
        fields = (
            'id', 'url', 'display', 'name', 'device_count', 'ip_count', 'vm_count', 'user_count',
            'ram_quota_used', 'cpu_quota_used', 'disk_quota_used', 'device_quota_used',
            'vm_quota_used', 'ip_quota_used'
        )


class NestedQuotaTemplateSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_project_quota-api:quotatemplate-detail'
    )

    class Meta:
        model = QuotaTemplate
        fields = ('id', 'url', 'display', 'template_name')

class ProjectSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_project_quota-api:project-detail'
    )
    quota_template = NestedQuotaTemplateSerializer()
    device_count = serializers.IntegerField(read_only=True)
    ip_count = serializers.IntegerField(read_only=True)
    vm_count = serializers.IntegerField(read_only=True)
    user_count = serializers.IntegerField(read_only=True)
    ram_quota_used = serializers.CharField(read_only=True)
    cpu_quota_used = serializers.CharField(read_only=True)
    disk_quota_used = serializers.CharField(read_only=True)
    device_quota_used = serializers.CharField(read_only=True)
    vm_quota_used = serializers.CharField(read_only=True)
    ip_quota_used = serializers.CharField(read_only=True)
    class Meta:
        model = Project
        fields = (
            'id', 'url', 'display', 'name', 'project_id', 'status', 'quota_template',
            'project_owner', 'description', 'device_count', 'ip_count', 'vm_count', 'user_count',
            'ram_quota_used', 'cpu_quota_used', 'disk_quota_used', 'device_quota_used',
            'vm_quota_used', 'ip_quota_used', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )


class QuotaTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_project_quota-api:quotatemplate-detail'
    )

    class Meta:
        model = QuotaTemplate
        lookup_field = 'template_name'
        fields = (
            'id', 'url', 'display', 'template_name', 'instances_quota',
            'vcpus_quota', 'ram_quota', 'ipaddr_quota', 'device_quota',
            'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )