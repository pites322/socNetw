# Generated by Django 2.2.2 on 2019-07-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_user_date_of_join'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_avatar_add',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not added'), (1, 'added')], default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_subscribe_to_somebody',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not added'), (1, 'added')], default=0, null=True),
        ),
    ]
