# Generated by Django 5.0.6 on 2024-05-15 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniApp', '0013_remove_rating_campus_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='RatingComment',
        ),
    ]
