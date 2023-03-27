# Generated by Django 4.1.6 on 2023-02-12 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles_app", "0002_relationship"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relationship",
            name="status",
            field=models.CharField(
                choices=[("request", "request"), ("accepted", "accepted")],
                max_length=10,
            ),
        ),
    ]