# Generated by Django 2.2.2 on 2019-07-11 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0006_subscribe_on_black_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_of_add',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
