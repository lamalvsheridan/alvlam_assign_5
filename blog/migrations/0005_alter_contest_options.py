# Generated by Django 4.1.2 on 2022-12-14 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_created_contest_submitted_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ['-submitted_date']},
        ),
    ]