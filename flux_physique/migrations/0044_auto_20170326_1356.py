# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0043_auto_20170321_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailstransfert',
            name='id_in_content_type',
            field=models.CharField(verbose_name='Id in content type', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='validation',
            unique_together=set([('id_in_content_type', 'content_type')]),
        ),
        migrations.AlterIndexTogether(
            name='validation',
            index_together=set([('id_in_content_type', 'content_type')]),
        ),
    ]
