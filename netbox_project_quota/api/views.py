from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import F

from .. import models
from .serializers import ProjectSerializer, QuotaTemplateSerializer
from django.db.models import Count, Subquery, OuterRef
from dcim.models import Device
from ipam.models import IPAddress
from virtualization.models import VirtualMachine

class ProjectViewSet(NetBoxModelViewSet):
    queryset = models.Project.objects.prefetch_related(
        'quota_template', 'tags'
    )
    
    def convert_mb_to_flexible_size(self, mb_value):
        if mb_value >= 1048576:
            # Convert from MB to TB
            tb_value = mb_value / 1024 / 1024
            return '{}TB'.format(int(tb_value))
        elif mb_value >= 1024:
            # Convert from MB to GB
            gb_value = mb_value / 1024
            return '{}GB'.format(int(gb_value))
        else:
            # No convert
            return '{}MB'.format(int(mb_value))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for project in queryset:
            project.device_count = project.devices.all().count()
            project.ip_count = project.ipaddress.all().count()
            project.vm_count = project.virtualmachine.all().count()
            project.user_count = project.contact.all().count()

            quota_templates = models.QuotaTemplate.objects.filter(id=project.quota_template_id).first()
            vms_list = project.virtualmachine.all()
            vms = VirtualMachine.objects.filter(
                    pk__in=[vm.pk for vm in vms_list]
                )
            result = vms.aggregate(total_ram=Sum('memory'), total_cpu=Sum('vcpus'))
            if result['total_cpu'] and result['total_ram']:
                total_cpu = result['total_cpu']
                total_ram = self.convert_mb_to_flexible_size(int(result['total_ram']))
            elif not result['total_cpu'] and not result['total_ram']:
                total_cpu = '0'
                total_ram = '0'
            elif result['total_cpu'] and not result['total_ram']:
                total_cpu = result['total_cpu']
                total_ram = '0'
            elif not result['total_cpu'] and result['total_ram']:
                total_cpu = '0'
                total_ram = self.convert_mb_to_flexible_size(int(result['total_ram']))

            if quota_templates.ram_quota:
                ram_quota = self.convert_mb_to_flexible_size(int(quota_templates.ram_quota))
            else:
                ram_quota = "_"
            project.ram_quota_used = "Assign {} of {}".format(
                str(total_ram),
                str(ram_quota)
            )

            if quota_templates.vcpus_quota:
                cpu_quota = quota_templates.vcpus_quota
            else:
                cpu_quota = "_"
            project.cpu_quota_used = "Assign {} of {}".format(
                int(total_cpu),
                str(cpu_quota)
            )

            project.disk_quota_used = "_"

            if quota_templates.device_quota:
                device_quota = quota_templates.device_quota
            else:
                device_quota = "_"
            project.device_quota_used = "Assign {} of {}".format(
                int(project.device_count),
                str(device_quota)
            )

            if quota_templates.instances_quota:
                vm_quota = quota_templates.instances_quota
            else:
                vm_quota = "_"
            project.vm_quota_used = "Assign {} of {}".format(
                int(project.vm_count),
                str(vm_quota)
            )

            if quota_templates.ipaddr_quota:
                ip_quota = quota_templates.ipaddr_quota
            else:
                ip_quota = "_"
            project.ip_quota_used = "Assign {} of {}".format(
                int(project.ip_count),
                str(ip_quota)
            )
            project.save()
        return queryset

    serializer_class = ProjectSerializer


class QuotaTemplateViewSet(NetBoxModelViewSet):
    queryset = models.QuotaTemplate.objects.prefetch_related('tags')
    serializer_class = QuotaTemplateSerializer
    # filterset_class = filtersets.ProjectFilterSet
