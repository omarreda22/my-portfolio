from pyexpat import model
from statistics import mode
from django.db import models
from django.db.models.fields import CharField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Recommended(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    main_image = models.ImageField(null=True, blank=True, upload_to="recommended", default="placeholder.png")
    go = models.URLField(max_length=200, null=True)
    def __str__(self):
        return self.headline

class Post(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    main_image = models.ImageField(null=True, blank=True, upload_to="images", default="placeholder.png")
    body = RichTextUploadingField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True, blank=True)
    live = models.URLField(max_length=200, null=True, blank=True)
    recommend = models.ManyToManyField(Recommended)
    num = models.CharField(default="0", null=True, blank=True, max_length=50)


    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.headline)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1 
                slug = slugify(self.headline) + '-' + str(count) 
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)