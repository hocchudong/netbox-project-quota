from extras.plugins import PluginConfig


class NetBoxManageProjectConfig(PluginConfig):
    name = 'netbox_project_quota'
    verbose_name = 'NetBox Manage Project Quota'
    description = 'Manage Create and Manage Project in Netbox'
    version = '1.0.7'
    base_url = 'netbox-project'
    min_version = '3.4.0'


config = NetBoxManageProjectConfig