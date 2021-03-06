# Generated by Django 2.2.1 on 2019-05-18 02:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_tittle', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('image', models.FileField(blank=True, null=True, upload_to='support/images')),
                ('support_type', models.CharField(choices=[('T', 'Technical'), ('PL', 'Plans'), ('M', 'Management'), ('D', 'Design'), ('A', 'Adverts'), ('P', 'Profile/ Account'), ('O', 'Others')], default='T', max_length=1)),
                ('viewed_by_ip', models.GenericIPAddressField(default='127.0.0.1')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=True)),
                ('viewed_at', models.DateTimeField(auto_now=True)),
                ('seen_by_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
