# Generated by Django 5.0 on 2024-06-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0007_rename_first_name_userprofile_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]