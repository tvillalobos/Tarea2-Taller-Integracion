# Generated by Django 3.2 on 2021-05-02 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapi', '0009_auto_20210502_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.TextField(),
        ),
    ]
