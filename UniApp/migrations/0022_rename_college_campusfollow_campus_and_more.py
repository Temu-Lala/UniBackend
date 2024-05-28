# Generated by Django 5.0.6 on 2024-05-16 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0021_campusfollow_departmentfollow_lecturerfollow_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campusfollow',
            old_name='college',
            new_name='campus',
        ),
        migrations.RenameField(
            model_name='departmentfollow',
            old_name='college',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='lecturerfollow',
            old_name='college',
            new_name='lecturer',
        ),
        migrations.RenameField(
            model_name='universityfollow',
            old_name='college',
            new_name='university',
        ),
    ]
