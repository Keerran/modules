# Generated by Django 2.1.5 on 2019-03-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190301_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.TextField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
