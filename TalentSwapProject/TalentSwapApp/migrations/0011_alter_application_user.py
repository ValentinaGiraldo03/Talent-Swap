# Generated by Django 5.0.2 on 2024-04-25 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TalentSwapApp', '0010_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applied_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
