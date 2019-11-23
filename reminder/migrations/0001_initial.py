# Generated by Django 2.2.7 on 2019-11-23 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FDAccountDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fd_name', models.CharField(max_length=100)),
                ('principal', models.IntegerField(default=0)),
                ('type_of_interest', models.IntegerField(choices=[(1, 'Simple Interest'), (2, 'Compound Interest')], default=1)),
                ('period', models.IntegerField(default=0)),
                ('time_of_interest', models.IntegerField(choices=[(1, 'monthly'), (2, 'Quarterly'), (3, 'Half Yearly'), (4, 'Annually')], default=1)),
                ('amount', models.FloatField(blank=True, default=0.0, null=True)),
                ('bank', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_amt', models.FloatField(blank=True, default=0.0, null=True)),
                ('month', models.DateField(auto_now=True, null=True)),
                ('is_sent', models.BooleanField(blank=True, default=False, null=True)),
                ('fd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reminder.FDAccountDetail')),
            ],
        ),
    ]
