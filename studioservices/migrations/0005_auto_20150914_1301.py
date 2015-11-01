# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studioservices', '0004_auto_20150904_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mrrfile',
            old_name='filename',
            new_name='base_name',
        ),
    ]
