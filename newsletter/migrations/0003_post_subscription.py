# Generated by Django 2.2.2 on 2019-06-25 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_auto_20190622_0108'),
        ('newsletter', '0002_auto_20190620_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('body', models.TextField()),
                ('short_description', models.CharField(blank=True, max_length=800, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_file', models.FileField(blank=True, upload_to='media/posts/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('mainimage', models.ImageField(blank=True, upload_to='media/')),
                ('number_of_click', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
