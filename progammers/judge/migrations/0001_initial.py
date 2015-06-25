# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('question', models.CharField(max_length=20000)),
                ('caption', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('s_id', models.IntegerField(serialize=False, primary_key=True)),
                ('status', models.IntegerField()),
                ('lang', models.CharField(max_length=200)),
                ('q_id', models.ForeignKey(to='judge.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('emailid', models.CharField(max_length=200, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='submission',
            name='u_id',
            field=models.ForeignKey(to='judge.User'),
            preserve_default=True,
        ),
    ]
