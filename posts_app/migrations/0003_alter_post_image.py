# Generated by Django 4.1.3 on 2023-03-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0002_alter_post_liked"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="posts"),
        ),
    ]
