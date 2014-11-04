# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpost_featured_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='featured_image',
        ),
    ]
