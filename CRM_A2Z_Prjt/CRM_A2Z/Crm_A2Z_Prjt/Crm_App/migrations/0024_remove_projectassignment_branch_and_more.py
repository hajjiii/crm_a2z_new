# Generated by Django 4.1.7 on 2023-04-27 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0023_remove_projectassignment_branch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectassignment',
            name='branch',
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='branch',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='Crm_App.branch'),
            preserve_default=False,
        ),
    ]