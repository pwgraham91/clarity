# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('speed_date', '0002_remove_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(related_name='user_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='user_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
