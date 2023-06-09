# Generated by Django 4.1.5 on 2023-03-10 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualization', '0034_standardize_description_comments'),
        ('dcim', '0167_module_status'),
        ('ipam', '0063_standardize_description_comments'),
        ('netbox_project_quota', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='devices',
        ),
        migrations.RemoveField(
            model_name='project',
            name='ipaddress',
        ),
        migrations.RemoveField(
            model_name='project',
            name='virtualmachine',
        ),
        migrations.AddField(
            model_name='project',
            name='devices',
            field=models.ManyToManyField(blank=True, default=None, related_name='assigned_device', to='dcim.device'),
        ),
        migrations.AddField(
            model_name='project',
            name='ipaddress',
            field=models.ManyToManyField(blank=True, default=None, related_name='assigned_ipaddress', to='ipam.ipaddress'),
        ),
        migrations.AddField(
            model_name='project',
            name='virtualmachine',
            field=models.ManyToManyField(blank=True, default=None, related_name='assigned_vm', to='virtualization.virtualmachine'),
        ),
    ]
