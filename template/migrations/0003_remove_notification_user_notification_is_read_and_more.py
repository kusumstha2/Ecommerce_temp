# Generated by Django 5.1.7 on 2025-03-18 08:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="user",
        ),
        migrations.AddField(
            model_name="notification",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="notification",
            name="user_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="created_at",
            field=models.DateTimeField(default=True),
        ),
    ]
