# Generated by Django 4.1.2 on 2022-10-21 10:21

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True, validators=[users.models.validate_age]),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=60, null=True, validators=[users.models.validate_email]),
        ),
    ]