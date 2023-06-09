# Generated by Django 4.1.5 on 2023-03-17 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0009_standardize_description_comments'),
        ('netbox_project_quota', '0003_project_contact_project_user_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='domain_name',
        ),
        migrations.AddField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.contact'),
        ),
    ]
