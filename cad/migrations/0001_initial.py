# Generated by Django 4.1.13 on 2023-11-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cad",
            fields=[
                (
                    "_id",
                    models.CharField(
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                        verbose_name="_id",
                    ),
                ),
                ("author", models.CharField(max_length=100)),
                ("mainCategory", models.CharField(max_length=255)),
                ("subCategory", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("index", models.TextField()),
                ("s3Url", models.TextField()),
                ("createdAt", models.DateTimeField()),
                ("_class", models.CharField(max_length=255)),
                ("classification", models.CharField(default="", max_length=255)),
                ("tfidf", models.TextField(blank=True, default="")),
            ],
            options={
                "db_table": "cad",
            },
        ),
    ]
