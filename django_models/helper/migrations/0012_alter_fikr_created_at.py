# Generated by Django 5.1 on 2024-08-09 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0011_alter_fikr_created_at_fikr_fikr_mark_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fikr',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 9, 17, 26, 18, 821657, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
