# Generated by Django 3.0.4 on 2020-09-15 19:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='shopuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='shopuser',
            name='last_name',
        ),
    ]
