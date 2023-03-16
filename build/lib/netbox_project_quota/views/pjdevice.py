from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Project
from .. import forms, tables
from django.db import transaction
from dcim.models import Device
from dcim.tables import DeviceTable
from dcim.filtersets import DeviceFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import sys


@register_model_view(Project, 'add_devices', path='devices/add')
class ProjectAddDevicesView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectAddDevicesForm
    template_name = 'project_views/project_add_devices.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        project = get_object_or_404(queryset)
        form = self.form(initial=request.GET)

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': reverse('plugins:netbox_project_quota:project', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        project = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():

            device_pks = form.cleaned_data['devices']
            with transaction.atomic():

                # Assign the selected Devices to the Project
                for device in Device.objects.filter(pk__in=device_pks):
                    if device in project.devices.all():
                        continue
                    else:
                        project.devices.add(device)
                        project.save()

            messages.success(request, "Added {} devices to project {}".format(
                len(device_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })


### Device Remove
@register_model_view(Project, 'remove_devices', path='devices/remove')
class ProjectRemoveDevicesView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectRemoveDevicesForm
    template_name = 'netbox_project_quota/generic/bulk_remove.html'

    def post(self, request, pk):

        project = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            device_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected Devices from the Project
                    for device in Device.objects.filter(pk__in=device_pks):
                        project.devices.remove(device)
                        project.save()

            messages.success(request, "Removed {} devices from Project {}".format(
                len(device_pks), project
            ))
            return redirect(project.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = Device.objects.filter(pk__in=pk_values)
        device_table = DeviceTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': project,
            'table': device_table,
            'obj_type_plural': 'devices',
            'return_url': project.get_absolute_url(),
        })


@register_model_view(Project, 'devices')
class ProjectDevicesView(generic.ObjectChildrenView):
    queryset = Project.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    template_name = 'project_views/device.html'
    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.devices.count() if obj.devices else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        device_list = parent.devices.all()
        return Device.objects.restrict(request.user, 'view').filter(
            pk__in=[device.pk for device in device_list]
        )