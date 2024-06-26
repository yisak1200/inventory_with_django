# Generated by Django 4.0.5 on 2023-03-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_code', models.IntegerField(unique=True)),
                ('asset_group', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Assets_tbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Asset_name', models.CharField(max_length=100)),
                ('Amout_of_asset', models.IntegerField()),
                ('Coast_of_single_asset', models.IntegerField()),
                ('Total_coast', models.IntegerField()),
                ('Receipt_number', models.CharField(max_length=100)),
                ('Asset_code_and_group', models.CharField(max_length=100)),
                ('measurment', models.CharField(max_length=20)),
                ('Asset_Inserted_date', models.DateTimeField(auto_now_add=True)),
                ('Assset_Registered_by', models.CharField(max_length=100)),
            ],
        ),
    ]
