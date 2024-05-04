# Generated by Django 5.0.4 on 2024-05-04 01:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0021_rename_campus_lecturercv_campus_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campuspost',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturercv'),
        ),
        migrations.AddField(
            model_name='collegepost',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturercv'),
        ),
        migrations.AddField(
            model_name='departmentpost',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturercv'),
        ),
        migrations.AddField(
            model_name='universitypost',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturercv'),
        ),
        migrations.CreateModel(
            name='LecturerPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='static/post_files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.campusprofile')),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.collegeprofile')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.departmentprofile')),
                ('lecturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturercv')),
                ('responding_to_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.lecturerpost')),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UniApp.universityprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]