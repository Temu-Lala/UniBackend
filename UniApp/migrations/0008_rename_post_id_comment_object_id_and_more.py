# Generated by Django 5.0.6 on 2024-05-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0007_delete_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='object_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
