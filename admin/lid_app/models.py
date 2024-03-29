from django.db import models


class Lid(models.Model):
    tg_id = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    school = models.CharField(max_length=15)
    class_num = models.CharField(max_length=15, null=True, blank=True)
    pinfl = models.CharField(max_length=50, null=True, blank=True)
    created_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    invitation = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'lids'
        ordering = ['-created_time']


class PostImage(models.Model):
    name = models.CharField(max_length=10, default='post')
    image_url = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image_url} - {self.active}"

    class Meta:
        db_table = 'images'
        ordering = ['-created_time']
