# Generated by Django 2.2.7 on 2019-11-25 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0004_fdaccountdetail_time_of_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='month',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]