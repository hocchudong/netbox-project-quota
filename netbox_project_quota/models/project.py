from django.db import models
from django.urls import reverse
from dcim.models import Device
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .quotatemplate import QuotaTemplate

class ProjectStatusChoices(ChoiceSet):

    CHOICES = [
        ('active', 'Active', 'blue'),
        ('disable', 'Disable', 'red'),
    ]


class Project(NetBoxModel):
    name = models.CharField(
        max_length=100
    )

    project_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name = 'Project ID'
    )

    project_owner = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name = 'Project Owner'
    )

    status = models.CharField(
        max_length=30,
        choices=ProjectStatusChoices
    )

    quota_template = models.ForeignKey(
        to='netbox_project_quota.QuotaTemplate',
        on_delete=models.SET_NULL,
        related_name='project_quota',
        null=True,
        verbose_name = 'Quota Template'
    )
    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='assigned_device',
        blank=True,
        default=None
    )
    ipaddress = models.ManyToManyField(
        to='ipam.IPAddress',
        related_name='assigned_ipaddress',
        blank=True,
        default=None
    )
    virtualmachine = models.ManyToManyField(
        to='virtualization.VirtualMachine',
        related_name='assigned_vm',
        blank=True,
        default=None
    )
    contact = models.ManyToManyField(
        to='tenancy.Contact',
        related_name='assigned_contact',
        blank=True,
        default=None
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )

    # Count Quota use
    device_count = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name = 'Device Count'
    )
    ip_count = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name = 'IP Count'
    )
    vm_count = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name = 'VM Count'
    )
    user_count = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name = 'User Count'
    )

    # Quota Used
    ram_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    cpu_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    disk_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    device_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    vm_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )
    ip_quota_used = models.CharField(
        max_length=100,
        null=True,
        default=None
    )

    # Comment
    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(f"{self.name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_project_quota:project', args=[self.pk])

    def get_status_color(self):
        return ProjectStatusChoices.colors.get(self.status)