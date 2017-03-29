# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0039_auto_20170316_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historiquedutravail',
            name='type',
        ),
        migrations.AlterField(
            model_name='historiquedutravail',
            name='employer',
            field=models.ForeignKey(verbose_name='Employé', to='refereces.Employer', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
