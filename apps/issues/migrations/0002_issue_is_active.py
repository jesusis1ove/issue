# Generated by Django 4.2.1 on 2023-05-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
