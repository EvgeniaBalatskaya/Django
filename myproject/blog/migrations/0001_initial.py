# Generated by Django 5.2.3 on 2025-07-06 12:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog_previews/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=False)),
                ('views_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Блоговая запись',
                'verbose_name_plural': 'Блоговые записи',
            },
        ),
    ]
