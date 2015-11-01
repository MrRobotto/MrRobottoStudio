# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studioservices', '0003_auto_20150823_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationattemp',
            name='user',
        ),
        migrations.DeleteModel(
            name='RegistrationAttemp',
        ),
    ]
