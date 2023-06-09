# Generated by Django 4.1.3 on 2022-12-14 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FavCategories',
                'managed': True,
            },
        ),
    ]
