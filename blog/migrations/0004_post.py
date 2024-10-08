# Generated by Django 4.2.7 on 2024-01-27 06:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_alter_profile_location_alter_profile_website"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "image",
                    models.ImageField(default=None, null=True, upload_to="post_images"),
                ),
                ("caption", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="blog.profile",
                    ),
                ),
            ],
        ),
    ]
