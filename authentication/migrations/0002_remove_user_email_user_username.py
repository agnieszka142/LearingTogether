# Generated by Django 4.1.3 on 2022-12-06 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='Bob_is_Back', max_length=255),
        ),
    ]
