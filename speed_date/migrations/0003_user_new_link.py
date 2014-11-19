# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speed_date', '0002_remove_user_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='new_link',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
