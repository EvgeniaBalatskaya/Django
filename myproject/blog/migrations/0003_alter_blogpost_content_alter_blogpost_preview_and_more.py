# Generated by Django 5.2.3 on 2025-07-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogpost_options_alter_blogpost_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='blog_previews/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
