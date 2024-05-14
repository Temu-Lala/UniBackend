# Generated by Django 5.0.6 on 2024-05-13 22:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0008_rename_post_id_comment_object_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='object_id',
            new_name='post_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]