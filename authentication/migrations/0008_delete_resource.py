# Generated by Django 5.1.1 on 2024-09-18 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0007_merge_20240918_1542"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Resource",
        ),
    ]
