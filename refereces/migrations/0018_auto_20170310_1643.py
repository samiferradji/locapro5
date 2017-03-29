# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0017_auto_20170221_1446'),
    ]

    def load_first_filiale(apps, schema_editor):
        Filiale = apps.get_model("refereces", "Filiale")
        new_filiale = Filiale(id=1, filiale='Hydrapahrm', prefix_filiale='HP')
        new_filiale.save()

    operations = [
        migrations.CreateModel(
            name='Filiale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('filiale', models.CharField(verbose_name='Nom de la filiale', max_length=30)),
                ('prefix_filiale', models.CharField(verbose_name='Préfix de codification', max_length=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='employer',
            options={'ordering': ['nom']},
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_boite',
            field=models.SmallIntegerField(verbose_name='Points par boites', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis',
            field=models.SmallIntegerField(verbose_name='Points par colis', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_colis_palettise',
            field=models.SmallIntegerField(verbose_name='Point par colis palettisés', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesmouvementstock',
            name='point_ligne',
            field=models.SmallIntegerField(verbose_name='Points par ligne', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesmouvementstock',
            name='description',
            field=models.TextField(verbose_name='Description du mouvement', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='typesmouvementstock',
            name='niveau',
            field=models.SmallIntegerField(verbose_name='Niveau de difficulté', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='magasin',
            name='filiale',
            field=models.ForeignKey(default=1, to='refereces.Filiale', verbose_name='Filiale'),
            preserve_default=False,
        ),
        migrations.RunPython(load_first_filiale)
    ]
