from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    interest = TaggableManager()
    bio_picture = models.FileField(blank=True)
    bio_text = models.TextField(help_text='Enter your bio details here.',default="Opps user didn't leave anything here!")

class Blog(models.Model):
    title = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    #title = models.CharField(max_length=50)
    song_name = models.CharField(max_length=50)
    song_src = models.CharField(max_length=200)
    #Blog_content = models.TextField(help_text='Enter your post here.')
    Blog_content = RichTextUploadingField(blank=False, null=False)
    create_time = models.DateTimeField(auto_now=True)
    last_edit_tiem = models.DateTimeField(auto_now=True)
    #picture = models.ForeignKey(Picture,on_delete=models.PROTECT)
    location = models.CharField(max_length=500)
    tags = TaggableManager()
    # isDraft = models.BooleanField(default=True)

class Picture(models.Model):
    picture_link = models.CharField(max_length=500,default='default_blog_picture.png')
    create_time = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog,default=None,on_delete=models.PROTECT)

def get_image_filename(instance, filename):
    title = instance.blog.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    comment_text = models.CharField(max_length=500,help_text='Enter your comment here. ')
    create_time = models.DateTimeField(auto_now=True)
