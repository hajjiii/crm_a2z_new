# Generated by Django 4.1.7 on 2023-04-27 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0020_remove_projectassignment_branch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectassignment',
            name='assign_globaly',
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='assign_globaly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assign_globaly', to='Crm_App.extendedusermodel'),
        ),
    ]
