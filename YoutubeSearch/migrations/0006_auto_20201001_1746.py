# Generated by Django 3.1.1 on 2020-10-01 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YoutubeSearch', '0005_auto_20200928_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodata',
            name='publishedAt',
            field=models.DateTimeField(db_index=True),
        ),
    ]
