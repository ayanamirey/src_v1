# Generated by Django 4.0.4 on 2022-05-12 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonMailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email подписчика')),
            ],
            options={
                'db_tablespace': 'common_mailing_list',
            },
        ),
        migrations.CreateModel(
            name='CaseMailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email подписчика')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case', verbose_name='Дело')),
            ],
            options={
                'db_tablespace': 'case_mailing_list',
            },
        ),
    ]
