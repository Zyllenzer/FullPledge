# Generated by Django 4.2 on 2023-09-17 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_bookupdates_delete_nonficbooksupdates'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookUpdates',
            new_name='BookUpdate',
        ),
    ]
