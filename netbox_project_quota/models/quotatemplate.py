from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


class QuotaTemplate(NetBoxModel):
    template_name = models.CharField(
        max_length=100,
        null=True,
        verbose_name = 'Template Quota'
    )

    instances_quota = models.PositiveIntegerField(
        null=True,
        verbose_name = 'VM Quota'
    )

    vcpus_quota = models.PositiveIntegerField(
        null=True,
        verbose_name = 'VCPUs Quota'
    )

    ram_quota = models.PositiveIntegerField(
        null=True,
        verbose_name = 'RAM Quota (MB)'
    )

    ipaddr_quota = models.PositiveIntegerField(
        null=True,
        verbose_name = 'IP Quota'
    )

    device_quota = models.PositiveIntegerField(
        null=True,
        verbose_name = 'Device Quota'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('template_name',)

    def __str__(self):
        return str(f"{self.template_name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_project_quota:quotatemplate', args=[self.pk])
