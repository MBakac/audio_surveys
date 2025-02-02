# Generated by Django 5.1.4 on 2025-01-03 03:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_surveys', '0002_audioexamples_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.JSONField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio_surveys.survey')),
            ],
        ),
    ]
