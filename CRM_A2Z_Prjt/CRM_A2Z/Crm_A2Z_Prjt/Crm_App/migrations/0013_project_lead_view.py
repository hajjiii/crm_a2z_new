# Generated by Django 4.1.7 on 2023-04-12 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0012_alter_notification_lead_alter_projectassignment_lead_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lead_view',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Crm_App.leadsview'),
        ),
    ]