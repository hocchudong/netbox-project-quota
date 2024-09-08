from netbox.views import generic
from .. import forms, models
from utilities.views import ViewTab, register_model_view
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext as _
from utilities.forms import ConfirmationForm
from tenancy.models import Contact
from tenancy.tables import ContactTable
from tenancy.filtersets import ContactFilterSet


@register_model_view(models.Project, 'add_contact', path='contact/add')
class ProjectAddContactView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectAddContactForm
    template_name = 'project_views/project_add_contact.html'

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

            contact_pks = form.cleaned_data['contact']
            with transaction.atomic():

                # Assign the selected Contact to the Project
                for contact in Contact.objects.filter(pk__in=contact_pks):
                    if contact in project.contact.all():
                        continue
                    else:
                        project.contact.add(contact)
                        project.save()

            messages.success(request, "Added {} contact to project {}".format(
                len(contact_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })

@register_model_view(models.Project, 'contact')
class ProjectContactView(generic.ObjectChildrenView):
    queryset = models.Project.objects.all()
    child_model = Contact
    table = ContactTable
    filterset = ContactFilterSet
    template_name = 'project_views/project_user_remove.html'
    tab = ViewTab(
        label=_('Users'),
        badge=lambda obj: obj.contact.count() if obj.contact else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        contact_list = parent.contact.all()
        return Contact.objects.restrict(request.user, 'view').filter(
            pk__in=[contact.pk for contact in contact_list]
        )

@register_model_view(models.Project, 'remove_contact', path='contact/remove')
class ProjectRemoveContactView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectContactRemoveForm
    template_name = 'netbox_project_quota/generic/bulk_remove.html'

    def post(self, request, pk):

        project = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            contact_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected Contacts from the Project
                    for contact in Contact.objects.filter(pk__in=contact_pks):
                        project.contact.remove(contact)
                        project.save()

            messages.success(request, "Removed {} contacts from Project {}".format(
                len(contact_pks), project
            ))
            return redirect(project.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = Contact.objects.filter(pk__in=pk_values)
        contact_table = ContactTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': project,
            'table': contact_table,
            'obj_type_plural': 'contact',
            'return_url': project.get_absolute_url(),
        })