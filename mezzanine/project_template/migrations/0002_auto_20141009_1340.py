# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
        ('project_template', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareableBlogPost',
            fields=[
                ('blogpost_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='blog.BlogPost')),
                ('visibility', models.IntegerField(choices=[(1, b'Public'), (2, b'Visible to Followers'), (3, b'Visible to selected Users or Communities')])),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpost', models.Model),
        ),
        migrations.CreateModel(
            name='StoryMakerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('private', models.BooleanField(default=False)),
                ('single_user', models.BooleanField(default=False)),
                ('invite_ony', models.BooleanField(default=False)),
                ('admins', models.ManyToManyField(related_name=b'administered_groups', to=settings.AUTH_USER_MODEL)),
                ('banned_users', models.ManyToManyField(related_name=b'banned_from_groups', to=settings.AUTH_USER_MODEL)),
                ('invited_users', models.ManyToManyField(related_name=b'invited_to_groups', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name=b'member_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shareableblogpost',
            name='visible_to',
            field=models.ManyToManyField(related_name=b'items_shared_with', null=True, to='project_template.StoryMakerGroup', blank=True),
            preserve_default=True,
        ),
    ]
