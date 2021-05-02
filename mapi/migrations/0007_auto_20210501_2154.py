# Generated by Django 3.2 on 2021-05-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapi', '0006_alter_album_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cid',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='artist',
            name='cid',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='cid',
            field=models.TextField(unique=True),
        ),
    ]
