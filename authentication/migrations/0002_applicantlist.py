# Generated by Django 4.0.2 on 2022-04-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='applicantList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('job_id', models.BigIntegerField()),
                ('appliedDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
