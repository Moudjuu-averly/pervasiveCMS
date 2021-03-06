# Generated by Django 2.2.2 on 2019-06-29 13:49

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20190629_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='repostjob',
            name='company',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repostjob',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='job_tittle', unique_with=['company', 'created']),
        ),
    ]
