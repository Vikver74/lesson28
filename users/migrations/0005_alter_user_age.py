# Generated by Django 4.1.2 on 2022-10-15 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers_user_date_joined_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
