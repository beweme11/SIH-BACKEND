# Generated by Django 5.1.3 on 2024-11-28 14:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalRegistry',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.TextField(blank=True, null=True)),
                ('court', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
                ('gpe', models.TextField(blank=True, null=True)),
                ('judge', models.TextField(blank=True, null=True)),
                ('lawyer', models.TextField(blank=True, null=True)),
                ('org', models.TextField(blank=True, null=True)),
                ('other_person', models.TextField(blank=True, null=True)),
                ('petitioner', models.TextField(blank=True, null=True)),
                ('precedent', models.TextField(blank=True, null=True)),
                ('provision', models.TextField(blank=True, null=True)),
                ('respondent', models.TextField(blank=True, null=True)),
                ('statute', models.TextField(blank=True, null=True)),
                ('witness', models.TextField(blank=True, null=True)),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ner_data', to='search.globalregistry')),
            ],
        ),
        migrations.CreateModel(
            name='SummaryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField()),
                ('file_name', models.TextField()),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary_data', to='search.globalregistry')),
            ],
        ),
    ]
