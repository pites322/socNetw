# Generated by Django 2.2.2 on 2019-07-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_remove_subscribe_on_black_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='on_black_list',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Using'), (0, "Doesn't use")], default=0, null=True),
        ),
    ]