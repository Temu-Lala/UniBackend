# Generated by Django 5.0.4 on 2024-05-03 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0020_rename_departmen_lecturercv_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecturercv',
            old_name='campus',
            new_name='campus_profile',
        ),
        migrations.RenameField(
            model_name='lecturercv',
            old_name='college',
            new_name='college_profile',
        ),
        migrations.RenameField(
            model_name='lecturercv',
            old_name='department',
            new_name='department_profile',
        ),
        migrations.RenameField(
            model_name='lecturercv',
            old_name='university',
            new_name='university_profile',
        ),
    ]