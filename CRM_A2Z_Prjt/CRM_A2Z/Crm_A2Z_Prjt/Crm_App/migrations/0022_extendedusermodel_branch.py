# Generated by Django 4.1.7 on 2023-04-27 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm_App', '0021_remove_projectassignment_assign_globaly_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedusermodel',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Crm_App.branch'),
            preserve_default=False,
        ),
    ]