# Generated by Django 4.1.7 on 2023-04-14 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0014_alter_project_lead_view_alter_templead_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='notes_about_client',
        ),
    ]