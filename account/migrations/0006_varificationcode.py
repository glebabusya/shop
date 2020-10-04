# Generated by Django 3.0.4 on 2020-10-02 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0005_shopuser_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='VarificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_key', models.CharField(max_length=6, unique=True)),
                ('attempt_amount', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
