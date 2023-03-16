from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Project
from .. import forms, tables
from django.db import transaction
from ipam.models import IPAddress
from ipam.tables import IPAddressTable
from ipam.filtersets import IPAddressFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(Project, 'ipaddress')
class ProjectIPAddressView(generic.ObjectChildrenView):
    queryset = Project.objects.all()
    child_model = IPAddress
    table = IPAddressTable
    filterset = IPAddressFilterSet
    template_name = 'project_views/ipaddress.html'
    tab = ViewTab(
        label=_('IPAddress'),
        badge=lambda obj: obj.ipaddress.count() if obj.ipaddress else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        ips_list = parent.ipaddress.all()
        return IPAddress.objects.restrict(request.user, 'view').filter(
            pk__in=[ipaddr.pk for ipaddr in ips_list]
        )



@register_model_view(Project, 'add_ipaddress', path='ipaddress/add')
class ProjectAddIPAddressView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectAddIPAddressForm
    template_name = 'project_views/project_add_ipaddress.html'

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
            ipaddress_pks = form.cleaned_data['ipaddress']
            with transaction.atomic():

                # Assign the selected IPAddress to the Project
                for ipaddress in IPAddress.objects.filter(pk__in=ipaddress_pks):
                    if ipaddress in project.ipaddress.all():
                        continue
                    else:
                        project.ipaddress.add(ipaddress)
                        project.save()

            messages.success(request, "Added {} ipaddress to project {}".format(
                len(ipaddress_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })


@register_model_view(Project, 'remove_ipaddress', path='ipaddress/remove')
class ProjectRemoveIPAddressView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectRemoveIPsForm
    template_name = 'netbox_project_quota/generic/bulk_remove.html'

    def post(self, request, pk):

        project = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            ips_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected IPs from the Project
                    for ips in IPAddress.objects.filter(pk__in=ips_pks):
                        project.ipaddress.remove(ips)
                        project.save()

            messages.success(request, "Removed {} ips from Project {}".format(
                len(ips_pks), project
            ))
            return redirect(project.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = IPAddress.objects.filter(pk__in=pk_values)
        ips_table = IPAddressTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': project,
            'table': ips_table,
            'obj_type_plural': 'ipaddress',
            'return_url': project.get_absolute_url(),
        })