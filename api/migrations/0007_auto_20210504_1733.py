# Generated by Django 3.2 on 2021-05-04 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210504_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteruser',
            name='account',
        ),
        migrations.AddField(
            model_name='user',
            name='twitterAcount',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.twitteruser'),
        ),
    ]
