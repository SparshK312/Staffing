# Generated by Django 4.2.4 on 2024-03-23 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0007_remove_waitlist_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitlist',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='waitlist',
            name='last_name',
        ),
    ]
