# Generated by Django 5.0.6 on 2024-05-11 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey', to='surveyApp.survey', verbose_name='принадлежность к опросу'),
        ),
    ]