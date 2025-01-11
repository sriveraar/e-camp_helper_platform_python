# Generated by Django 5.1.4 on 2025-01-11 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.service')),
            ],
        ),
        migrations.AddField(
            model_name='provider',
            name='services',
            field=models.ManyToManyField(through='providers.ProviderService', to='providers.service'),
        ),
    ]