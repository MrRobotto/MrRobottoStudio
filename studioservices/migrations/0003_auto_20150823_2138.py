# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studioservices', '0002_auto_20150823_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mrrfile',
            old_name='selected',
            new_name='is_selected',
        ),
    ]
