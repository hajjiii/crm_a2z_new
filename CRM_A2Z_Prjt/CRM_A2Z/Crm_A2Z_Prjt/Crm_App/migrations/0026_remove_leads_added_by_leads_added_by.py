# Generated by Django 4.1.7 on 2023-04-01 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0025_remove_leads_added_by_leads_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='added_by',
        ),
        migrations.AddField(
            model_name='leads',
            name='added_by',
            field=models.ManyToManyField(blank=True, to='Crm_App.extendedusermodel'),
        ),
    ]
