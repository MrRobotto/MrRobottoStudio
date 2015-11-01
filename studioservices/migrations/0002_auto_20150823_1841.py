# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studioservices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MrrFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('filename', models.CharField(max_length=80)),
                ('blend_file', models.FileField(upload_to='')),
                ('mrr_file', models.FileField(upload_to='')),
                ('selected', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='blendfile',
            name='user',
        ),
        migrations.DeleteModel(
            name='BlendFile',
        ),
    ]
