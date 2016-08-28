# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Logged at')),
                ('logger', models.CharField(max_length=50, verbose_name='Logger')),
                ('lvl', models.CharField(max_length=20, verbose_name='Level')),
                ('msg', models.TextField(verbose_name='Message')),
                ('gid', models.CharField(max_length=200, verbose_name='Group ID')),
                ('mid', models.CharField(max_length=200, verbose_name='Message ID')),
                ('pid', models.CharField(max_length=200, null=True, verbose_name='Parent ID')),
                ('props', models.TextField(verbose_name='Properties')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
            },
        ),
    ]
