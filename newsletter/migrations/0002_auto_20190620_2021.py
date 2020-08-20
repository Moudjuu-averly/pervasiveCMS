# Generated by Django 2.2.1 on 2019-06-20 20:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('-created',)},
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(default=datetime.datetime(2019, 6, 20, 20, 21, 7, 20665, tzinfo=utc), max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='contact',
            name='full_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='contact',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(max_length=1250),
        ),
    ]
