# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speed_date', '0003_user_new_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='new_link',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
