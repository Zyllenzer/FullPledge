# Generated by Django 4.2 on 2023-08-21 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_usersite_permission_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=250)),
                ('current_page', models.IntegerField()),
                ('last_page', models.IntegerField()),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usersite')),
            ],
        ),
    ]
