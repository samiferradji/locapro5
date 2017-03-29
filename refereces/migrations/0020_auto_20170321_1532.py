# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0019_auto_20170311_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='prelevement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Emplacement de prélèvement', to='refereces.Emplacement'),
        ),
    ]
