# Generated by Django 2.1.5 on 2019-03-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_module_par'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.TextField(max_length=12, primary_key=True, serialize=False),
        ),
    ]
