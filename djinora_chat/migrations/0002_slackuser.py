# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djinora_chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('uid', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
