# Generated by Django 4.2.7 on 2024-01-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_profile_dob_profile_website_alter_profile_bio_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="website",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]