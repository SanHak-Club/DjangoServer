# Generated by Django 4.1.13 on 2023-11-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cad", "0003_rename_classification_cad_cadlabel_alter_cad_tfidf"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cad",
            name="_id",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
