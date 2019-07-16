# Generated by Django 2.1.5 on 2019-04-27 21:21

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('song_name', models.CharField(max_length=50)),
                ('song_src', models.CharField(max_length=200)),
                ('Blog_content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('last_edit_tiem', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=500)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(help_text='Enter your comment here. ', max_length=500)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PittsTime.Blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture_link', models.CharField(default='default_blog_picture.png', max_length=500)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='PittsTime.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio_picture', models.FileField(blank=True, upload_to='')),
                ('bio_text', models.TextField(default="Opps user didn't leave anything here!", help_text='Enter your bio details here.')),
                ('interest', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
