# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0016_magasin_type_entreposage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='code_rh',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='code_employee',
            field=models.ForeignKey(default=1, to='refereces.Employer', verbose_name='Code Employé'),
            preserve_default=False,
        ),
    ]
