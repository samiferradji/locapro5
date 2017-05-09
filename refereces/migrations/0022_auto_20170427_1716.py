# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0021_produitadresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='code_employee',
            field=models.ForeignKey(to='refereces.Employer', null=True, verbose_name='Code Employé'),
        ),
    ]
