# Generated by Django 4.2.7 on 2024-02-02 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_post_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, default=None, null=True, upload_to="post_images"
            ),
        ),
    ]
