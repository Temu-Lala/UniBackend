# Generated by Django 5.0.6 on 2024-05-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0036_remove_labprofile_files_labfile_lab_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='labprofile',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
