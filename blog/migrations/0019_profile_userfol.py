# Generated by Django 5.0.4 on 2024-04-14 15:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0018_profile_about"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="userfol",
            field=models.ManyToManyField(
                related_name="userfollowing", to="blog.profile"
            ),
        ),
    ]
