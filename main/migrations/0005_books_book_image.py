# Generated by Django 4.2 on 2023-08-21 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='book_image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/book-img/'),
        ),
    ]
