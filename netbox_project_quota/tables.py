import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from .models import Project, QuotaTemplate


__all__ = (
    'ProjectTable',
    'QuotaTemplateTable',
)

class ProjectTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    project_id = tables.Column()

    project_owner = tables.Column(
        linkify=True,
    )

    status = ChoiceFieldColumn()

    quota_template = tables.Column(
        linkify=True,
    )

    device_count = tables.Column()

    ip_count = tables.Column()

    vm_count = tables.Column()

    user_count = tables.Column()

    description = tables.Column()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Project
        fields = ("pk",
                  "id",
                  "name",
                  "project_id",
                  "project_owner",
                  "status",
                  "quota_template",
                  "device_count",
                  "ip_count",
                  "vm_count",
                  "user_count",
                  "ram_quota_used",
                  "cpu_quota_used",
                  "disk_quota_used",
                  "device_quota_used",
                  "vm_quota_used",
                  "ip_quota_used",
                  "description",
                  "comments",
                  "tags",
                  "created",
                  "last_updated",
                  "actions"
                )
        default_columns = ("name",
                           "project_owner",
                           "status",
                           "quota_template",
                           "device_count",
                           "ip_count",
                           "vm_count",
                           "user_count",
                           "description"
                        )

class QuotaTemplateTable(NetBoxTable):
    template_name = tables.Column(
        linkify=True,
    )

    instances_quota = tables.Column()

    vcpus_quota = tables.Column()

    ram_quota = tables.Column()

    ipaddr_quota = tables.Column()

    device_quota = tables.Column()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = QuotaTemplate
        fields = (
            'id',
            'template_name',
            'instances_quota',
            'vcpus_quota',
            'ram_quota',
            'ipaddr_quota',
            'device_quota',
            'description',
            'comments',
            'tags',
            'created',
            'last_updated',
            'actions',
        )
        default_columns = (
            'template_name',
            'instances_quota',
            'vcpus_quota',
            'ram_quota',
            'ipaddr_quota',
            'device_quota',
            'description'
        )