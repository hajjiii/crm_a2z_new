# Generated by Django 4.1.7 on 2023-03-29 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0018_alter_leadsview_temp_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='exit_lead_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
