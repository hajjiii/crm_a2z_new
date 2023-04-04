# Generated by Django 4.1.7 on 2023-04-01 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0024_remove_leads_added_by_alter_leads_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='added_by',
        ),
        migrations.AddField(
            model_name='leads',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Crm_App.extendedusermodel'),
        ),
    ]
