# Generated by Django 2.2.2 on 2019-07-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_chatslistcurrentmessage_date_of_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_of_add',
            field=models.DateTimeField(),
        ),
    ]