# Generated by Django 4.1.3 on 2022-12-07 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_user_id_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='ID_USER',
            new_name='user_id',
        ),
    ]
