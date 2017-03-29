# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0020_auto_20170321_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProduitAdresses',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=20, serialize=False)),
                ('produit', models.CharField(max_length=200)),
                ('adresse', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tempo_adresses',
                'managed': False,
            },
        ),
    ]
