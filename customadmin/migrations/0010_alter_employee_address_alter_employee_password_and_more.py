# Generated by Django 4.2.2 on 2023-06-28 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0009_messaging'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='post',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='employee_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
