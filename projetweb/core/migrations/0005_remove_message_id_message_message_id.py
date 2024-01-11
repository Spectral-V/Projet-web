# Generated by Django 4.1 on 2024-01-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_permission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="id",
        ),
        migrations.AddField(
            model_name="message",
            name="message_id",
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]