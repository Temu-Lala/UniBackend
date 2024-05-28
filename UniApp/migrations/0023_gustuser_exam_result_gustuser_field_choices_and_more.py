# Generated by Django 5.0.6 on 2024-05-20 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0022_rename_college_campusfollow_campus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gustuser',
            name='exam_result',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gustuser',
            name='field_choices',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gustuser',
            name='health_condition',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
