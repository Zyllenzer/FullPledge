# Generated by Django 4.2 on 2023-08-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=250, unique=True)),
                ('email', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=1024)),
            ],
        ),
    ]