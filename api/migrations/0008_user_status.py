# Generated by Django 3.2 on 2021-05-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210504_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(choices=[(True, 'Doctor'), (False, 'Patient')], default=False),
        ),
    ]
