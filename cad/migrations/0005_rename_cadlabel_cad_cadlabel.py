# Generated by Django 4.1.13 on 2023-11-13 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cad', '0004_alter_cad__id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cad',
            old_name='CadLabel',
            new_name='cadLabel',
        ),
    ]
