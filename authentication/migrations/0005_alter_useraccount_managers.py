# Generated by Django 5.1.1 on 2024-09-17 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_remove_useraccount_name_remove_useraccount_username"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="useraccount",
            managers=[],
        ),
    ]
