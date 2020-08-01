# Generated by Django 3.0.8 on 2020-08-01 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviecoll', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
        migrations.AddField(
            model_name='movie',
            name='collection',
            field=models.ManyToManyField(to='moviecoll.Collection'),
        ),
    ]
