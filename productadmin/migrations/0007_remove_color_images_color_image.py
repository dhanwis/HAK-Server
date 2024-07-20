# Generated by Django 5.0.2 on 2024-07-20 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productadmin', '0006_alter_colorimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='images',
        ),
        migrations.AddField(
            model_name='color',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productadmin.colorimage'),
        ),
    ]
