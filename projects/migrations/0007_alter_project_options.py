# Generated by Django 4.0 on 2021-12-20 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20211207_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-votes_total', 'title']},
        ),
    ]
