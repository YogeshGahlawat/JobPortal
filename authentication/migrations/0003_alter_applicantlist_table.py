# Generated by Django 4.0.2 on 2022-04-02 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_applicantlist'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='applicantlist',
            table='applicant',
        ),
    ]