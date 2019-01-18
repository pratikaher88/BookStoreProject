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
from django.core.validators import RegexValidator


CONITION_CHOICES = (
    ('Acceptable', 'Acceptable'),
    ('Bad', 'Bad'),
    ('Good', 'Good'),
)
ZIP_CHOICES = (
    ('421202', '421202'),
    ('421201', '421201'),
    ('421203', '421203'),
)
BUY_OR_EXCHANGE = (
    ('Sell', 'Sell'),
 ('Exchange', 'Exchange'), 
 )

def random_img():
    dir_path = os.path.join(BASE_DIR, 'media')
    files = [content for content in listdir(
        dir_path) if isfile(path_join(dir_path, content))]
    return str(choice(files))

class Book(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000,blank=True,null=True)
    image = models.ImageField(null=True, blank=True, upload_to="book_images/")
    price = models.IntegerField(null=True,blank=True)
    sell_or_exchange = models.CharField(
        max_length=100, choices=BUY_OR_EXCHANGE, default='Exchange')
    condition = models.CharField(
        max_length=100, choices=CONITION_CHOICES, default='Acceptable')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.book_name
    
    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            output_size = (120, 120)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default=random_img , upload_to="profile_images/")

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class ShippingAddress(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE,related_name='address')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17)
    flatnumber = models.CharField("Flat Number", max_length=100)
    address1 = models.CharField("Address line 1", max_length=500,)
    address2 = models.CharField("Address line 2", max_length=500,blank=True,null=True)
    zip_code = models.CharField(
        max_length=100, choices=ZIP_CHOICES ,default='421202')
    city = models.CharField("City", max_length=100,)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def status(self):
        return self.address1 is "" or self.phone_number is ""

    def __str__(self):
        return "{},{},{},{},{}".format(self.flatnumber, self.address1, self.address2, self.zip_code, self.city)

class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Book)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def __str__(self):
        return self.owner.user.username

class UserCollection(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    books = models.ManyToManyField(Book)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_collection_items(self):
        return self.books.all()

    def __str__(self):
        return self.owner.user.username

class Requests(models.Model):

	requester = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	offerrer = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	requester_book = models.ForeignKey(Book, related_name='requester_book_from_user', on_delete=models.CASCADE)

	def __str__(self):
	    return "Request from {}, to {} ,with Book {}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name)

    # class Meta:
    #     verbose_name_plural = "Requests"

class Transaction(models.Model):

	requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
	offerrer = models.ForeignKey(User, related_name='offerrer', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	requester_book = models.ForeignKey(Book, related_name='requested_book_from_user', on_delete=models.CASCADE)
	offerrer_book = models.ForeignKey(Book, related_name='offerrer_book_from_user', on_delete=models.CASCADE)

	def __str__(self):
		return "From {}, to {} Book1 is {} Book2 is{}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name, self.offerrer_book.book_name)

class OldRequests(models.Model):

	requester = models.ForeignKey(User, related_name='old_to_user', on_delete=models.CASCADE)
	offerrer = models.ForeignKey(User, related_name='old_from_user', on_delete=models.CASCADE)
	requester_book = models.ForeignKey( Book, related_name='old_requester_book_from_user', on_delete=models.CASCADE, )

	def __str__(self):
	    return "From {}, to {} ,with Book {}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name)

class FinalBuyOrder(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    book = models.OneToOneField(Book , on_delete=models.CASCADE)
    seller = models.OneToOneField(
        User, related_name='seller',  on_delete=models.CASCADE)
    useraddress = models.OneToOneField(
        ShippingAddress, related_name='address', on_delete=models.CASCADE)
    selleraddress = models.OneToOneField(ShippingAddress, related_name='selleraddress', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.book_name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Order.objects.create(owner=instance.profile)
        ShippingAddress.objects.create(profile=instance.profile)
        UserCollection.objects.create(owner=instance.profile)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

