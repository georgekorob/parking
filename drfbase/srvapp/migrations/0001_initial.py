# Generated by Django 3.2.12 on 2022-02-22 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servername', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=16)),
                ('port', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'ai сервер',
                'verbose_name_plural': 'ai сервера',
            },
        ),
        migrations.CreateModel(
            name='ANServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servername', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=16)),
                ('port', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'an сервер',
                'verbose_name_plural': 'an сервера',
            },
        ),
        migrations.CreateModel(
            name='CAMServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servername', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=16)),
                ('port', models.PositiveIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'cam сервер',
                'verbose_name_plural': 'cam сервера',
            },
        ),
    ]
