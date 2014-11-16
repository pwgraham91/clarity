# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speed_date', '0004_user_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='preference',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
