# Generated by Django 4.1.3 on 2022-12-06 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
