# Generated by Django 4.2.5 on 2023-09-23 15:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_options_remove_habit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время'),
            preserve_default=False,
        ),
    ]
