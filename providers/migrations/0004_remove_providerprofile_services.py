# Generated by Django 5.1.4 on 2025-01-11 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_alter_provider_email_providerprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providerprofile',
            name='services',
        ),
    ]
