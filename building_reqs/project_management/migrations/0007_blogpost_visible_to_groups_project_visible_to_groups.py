# Generated by Django 5.1.2 on 2024-11-06 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project_management', '0006_map_maplink'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='visible_to_groups',
            field=models.ManyToManyField(blank=True, related_name='visible_blogposts', to='auth.group'),
        ),
        migrations.AddField(
            model_name='project',
            name='visible_to_groups',
            field=models.ManyToManyField(blank=True, related_name='visible_projects', to='auth.group'),
        ),
    ]
