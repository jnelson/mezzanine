# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blogpost_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='featured_image',
            field=mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Featured Image', blank=True),
            preserve_default=True,
        ),
    ]
