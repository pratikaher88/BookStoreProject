from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from random import choice
from os.path import join as path_join
from os import listdir
import os
from os.path import isfile
from nofapapp.settings import BASE_DIR

CONITION_CHOICES = (
    ('Acceptable', 'Acceptable'),
    ('Bad', 'Bad'),
    ('Good', 'Good'),
)


def random_img():
    dir_path = os.path.join(BASE_DIR, 'media')
    files = [content for content in listdir(
        dir_path) if isfile(path_join(dir_path, content))]
    return str(choice(files))


class Book(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image = models.ImageField(null=True, blank=True, upload_to="book_images/")
    price = models.IntegerField()
    condition = models.CharField(
        max_length=100, choices=CONITION_CHOICES, default='Acceptable')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.book_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default=random_img(), upload_to="profile_images/")

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class OrderItem(models.Model):
    book = models.OneToOneField(
        Book, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.book_name


class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def __str__(self):
        return self.owner.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=Book)
# def create_user_list(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# class UserBooks(models.Model):

#     user = models.ForeignKey(User ,on_delete = models.CASCADE ,null=True)
#     book = models.ManyToManyField( Book )

#     def __str__(self):
#         return self.book_name
