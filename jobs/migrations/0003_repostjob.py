# Generated by Django 2.2.2 on 2019-06-29 13:44

import autoslug.fields
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20190622_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='RePostJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_tittle', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='job_tittle', unique_with=['user', 'created'])),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('job_type', models.CharField(choices=[('F', 'Full time'), ('P', 'Part time'), ('C', 'Contract'), ('L', 'Freelancer'), ('I', 'Internship'), ('V', 'Volunteer')], default='F', max_length=1)),
                ('location', models.CharField(choices=[('O', 'Office'), ('R', 'Remote')], default='O', max_length=15)),
                ('job_video', models.FileField(blank=True, null=True, upload_to='images/jobs/job_image')),
                ('rating', models.FloatField(null=True)),
                ('views', models.IntegerField(blank=True, default=0, null=True)),
                ('view_by', models.GenericIPAddressField(default='')),
                ('deleted', models.BooleanField(default=False)),
                ('edited', models.BooleanField(default=False)),
                ('min_salary', models.FloatField(default=150.0)),
                ('max_salary', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(null=True)),
                ('last_edited', models.DateTimeField(auto_now=True)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created', '-last_edited'),
            },
        ),
    ]
