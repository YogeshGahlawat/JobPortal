# Generated by Django 4.0.2 on 2022-03-30 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='jobDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_id', models.PositiveBigIntegerField()),
                ('jobType', models.CharField(max_length=255)),
                ('jobProfile', models.CharField(max_length=255)),
                ('jobLocation', models.CharField(max_length=255)),
                ('offeringSalary', models.CharField(max_length=255, null=True)),
                ('postedDate', models.DateTimeField(auto_now_add=True)),
                ('validUpto', models.DateTimeField()),
                ('user_id', models.PositiveBigIntegerField()),
                ('postedBy', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'jobDetails',
            },
        ),
        migrations.CreateModel(
            name='organisationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisationName', models.CharField(max_length=255)),
                ('officeAddress', models.CharField(max_length=255)),
                ('organisationSize', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'organisationDetails',
            },
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.URLField(null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('SELECT', ''), ('MALE', 'Male'), ('FEMALE', 'Female'), ('TRANSGENDER', 'Transgender')], max_length=11, null=True)),
                ('birth_date', models.DateField(null=True)),
                ('joining_date', models.DateField(auto_now=True)),
                ('address', models.TextField(null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]