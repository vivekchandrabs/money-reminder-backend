# Generated by Django 2.2.7 on 2019-11-25 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0003_fdaccountdetail_rate_of_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='fdaccountdetail',
            name='time_of_interest',
            field=models.IntegerField(choices=[(1, 'monthly'), (2, 'Quarterly'), (3, 'Half Yearly'), (4, 'Annually')], default=1),
        ),
    ]
