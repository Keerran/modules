# Generated by Django 2.1.5 on 2019-01-24 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_module_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='module',
            old_name='parent',
            new_name='par',
        ),
        migrations.AddField(
            model_name='parent',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='app.Module'),
        ),
        migrations.AddField(
            model_name='parent',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='app.Module'),
        ),
    ]
