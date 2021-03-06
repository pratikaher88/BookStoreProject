from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete ,pre_delete
from django.dispatch import receiver
from PIL import Image
from random import choice
from os.path import join as path_join
from os import listdir
import os
import requests
from os.path import isfile
from nofapapp.settings import BASE_DIR, MAILGUN_KEY, MAILGUN_REQUEST_URL, MSG_SMS_URL, MSG_SMS_AUTH_KEY
from django.core.validators import RegexValidator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import threading

CONITION_CHOICES = (
    ('Almost New', 'Almost New'),
    ('Acceptable', 'Acceptable'),
    ('Good', 'Good'),
    ('Bad', 'Bad'),
)
ZIP_CHOICES = (
    ('421202', '421202'),
    ('421201', '421201'),
    ('421204', '421204'),
    ('421203', '421203'),
    ('421301', '421301'),

)
BUY_OR_EXCHANGE = (
    ('Sell', 'Sell'),
    ('Exchange', 'Exchange'),
)


def random_img():
    dir_path = os.path.join(BASE_DIR, 'static/profile_pic')
    files = [content for content in listdir(
        dir_path) if isfile(path_join(dir_path, content))]
    return str(choice(files))


class Book(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(
        max_length=100, help_text="We only deal with original books with ISBN codes, pirated books will not be accepted.")
    author_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    # image = models.ImageField('Book Image', null=True,
    #                           blank=True, upload_to="book_images/")
    price = models.IntegerField(
        null=True, blank=True, help_text="We would be deducting 20 rupees from item price for delivery purposes.")
    sell_or_exchange = models.CharField(
        max_length=100, choices=BUY_OR_EXCHANGE, default='Exchange', help_text="By adding items to exchange you can make requests to other users for exchange.")
    condition = models.CharField(
        max_length=100, choices=CONITION_CHOICES, default='Acceptable')
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=500,blank=True,null=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.book_name

    # def save(self, *args, **kwargs):
    #     super(Book, self).save(*args, **kwargs)
    #     if self.image:
    #         img = Image.open(self.image.path)
    #         output_size = (120, 120)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default=random_img, upload_to="profile_images/")

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
        Profile, on_delete=models.CASCADE, related_name='address')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, help_text="Enter your 10 digit phone number without any prefix code.")
    flatnumber = models.CharField("Flat Number", max_length=100)
    address1 = models.CharField("Address line 1", max_length=500,)
    address2 = models.CharField(
        "Address line 2", max_length=500, blank=True, null=True)
    zip_code = models.CharField(
        max_length=100, choices=ZIP_CHOICES, default='421202', help_text="We only operate in these locations for now!")
    city = models.CharField("City", max_length=100,)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def status(self):
        return self.address1 is "" or self.phone_number is ""

    def __str__(self):
        return "{},{},{},{},{},{}".format(self.profile.user.username,self.flatnumber, self.address1, self.address2, self.zip_code, self.phone_number)


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

    requester = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
    offerrer = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    requester_book = models.ForeignKey(
        Book, related_name='requester_book_from_user', on_delete=models.CASCADE)

    def __str__(self):
        return "Request from {}, to {} ,with Book {}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name)

    class Meta:
        verbose_name_plural = "Requests"


class Transaction(models.Model):

    requester = models.ForeignKey(
        User, related_name='requester', on_delete=models.CASCADE)
    offerrer = models.ForeignKey(
        User, related_name='offerrer', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    requester_book = models.ForeignKey(
        Book, related_name='requested_book_from_user', on_delete=models.CASCADE)
    offerrer_book = models.ForeignKey(
        Book, related_name='offerrer_book_from_user', on_delete=models.CASCADE)
    requester_address = models.ForeignKey(
        ShippingAddress, related_name='user_address', null=True, on_delete=models.CASCADE)
    offerrer_address = models.ForeignKey(
        ShippingAddress, related_name='seller_address', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "From {}, to {} and  {} to {}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name, self.offerrer_book.book_name)


class OldRequests(models.Model):

    requester = models.ForeignKey(
        User, related_name='old_to_user', on_delete=models.CASCADE)
    offerrer = models.ForeignKey(
        User, related_name='old_from_user', on_delete=models.CASCADE)
    requester_book = models.ForeignKey(
        Book, related_name='old_requester_book_from_user', on_delete=models.CASCADE, )

    def __str__(self):
        return "From {}, to {} ,with Book {}".format(self.requester.username, self.offerrer.username, self.requester_book.book_name)

    class Meta:
        verbose_name_plural = "Old Requests"

class FinalBuyOrder(models.Model):
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        User, related_name='seller',  on_delete=models.CASCADE)
    useraddress = models.ForeignKey(
        ShippingAddress, related_name='address', on_delete=models.CASCADE)
    selleraddress = models.ForeignKey(
        ShippingAddress, related_name='selleraddress', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True)

    def __str__(self):
        return self.book.book_name


class CompletedTransaction(models.Model):

    requester = models.ForeignKey(
        User, related_name='completed_requester', on_delete=models.CASCADE)
    offerrer = models.ForeignKey(
        User, related_name='completed_offerrer', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    requester_book_name = models.CharField(max_length=100, blank=True, null=True)

    offerrer_book_name = models.CharField(
        max_length=100, blank=True, null=True)
    
    requester_author_name = models.CharField(
        max_length=100, blank=True, null=True)

    offerrer_author_name = models.CharField(
        max_length=100, blank=True, null=True)
    
    requester_address = models.ForeignKey(
        ShippingAddress, related_name='completed_user_address', null=True, on_delete=models.CASCADE)
    offerrer_address = models.ForeignKey(
        ShippingAddress, related_name='completed_seller_address', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "From {}, to {} Book1 is {} Book2 is{}".format(self.requester.username, self.offerrer.username, self.requester_book_name, self.offerrer_book_name)



class CompletedBuyOrder(models.Model):
	user = models.ForeignKey(User, related_name='completed_user',
	                         blank=True, null=True, on_delete=models.CASCADE)
	book_name = models.CharField(max_length=100, blank=True, null=True)
	author_name = models.CharField(max_length=100, blank=True, null=True)
	seller = models.ForeignKey(
		User, related_name='completed_seller', blank=True, null=True,  on_delete=models.CASCADE)
	useraddress = models.ForeignKey(
		ShippingAddress, related_name='completed_address', blank=True, null=True, on_delete=models.CASCADE)
	selleraddress = models.ForeignKey(
		ShippingAddress, related_name='completed_selleraddress', blank=True, null=True, on_delete=models.CASCADE)
	date_ordered = models.DateTimeField(auto_now_add=True)
	total_price = models.IntegerField(null=True)

	def __str__(self):
		return self.book_name

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


# class EmailThread(threading.Thread):
#     def __init__(self, subject, html_content, recipient_list):
#         self.subject = subject
#         self.recipient_list = recipient_list
#         self.html_content = html_content
#         threading.Thread.__init__(self)

#     def run(self):
#         msg = EmailMessage(self.subject, self.html_content, to=self.recipient_list)
#         msg.send()

class EmailThreadAPI(threading.Thread):
    def __init__(self, subject, text, recepient):
        self.subject = subject
        self.text = text
        self.recepient = recepient
        threading.Thread.__init__(self)

    def run(self):
        requests.post(MAILGUN_REQUEST_URL, auth=('api', MAILGUN_KEY), data={
            'from': 'cadabrabooks@gmail.com',
            'to': self.recepient,
            'subject': self.subject,
            'text': self.text,
        })

def send_sms(mobiles,message):
    parms = {
        'authkey': MSG_SMS_AUTH_KEY,
        'country': '91',
        'sender': 'CDABRA',
        'route': '4',
        'mobiles': mobiles,
        'message': message,
    }
    request = requests.post(url=MSG_SMS_URL, params=parms)

# Done
@receiver(post_save, sender=Transaction)
def send_transaction_email(sender, instance, created, **kwargs):

    if created:

        EmailThreadAPI(subject='Exchange Order created for your book ' + instance.offerrer_book.book_name,
                       text='An exchange order has been created for "' + instance.requester_book.book_name +
                                           '" from "' + instance.requester.username +
                                           '" and "'+instance.offerrer_book.book_name +
                                           '" from "' + instance.offerrer.username +
                                           '". Go to  https://www.cadabra.co.in/transaction/orders/ to view the order. Thank You for ordering. Delivery of your book order will be attempted by CADABRA within one week.',
                                        recepient=instance.offerrer.email).start()

        EmailThreadAPI(subject='Exchange Order created for your book ' + instance.requester_book.book_name,
                       text='An exchange order has been created for "' + instance.requester_book.book_name +
                       '" from "' + instance.requester.username +
                       '" and "'+instance.offerrer_book.book_name +
                       '" from "' + instance.offerrer.username +
                       '". Go to  https://www.cadabra.co.in/transaction/orders/ to view the order. Thank You for ordering. Delivery of your book order will be attempted by CADABRA within one week.',
                       recepient=instance.requester.email).start()

        send_sms(mobiles=instance.offerrer_address.phone_number, message='An exchange order has been created for "' + instance.requester_book.book_name +
                 '" from  user ' + instance.requester.username +
                 ' and "'+instance.offerrer_book.book_name +
                 '" from user ' + instance.offerrer.username +
                 '. Go to  https://www.cadabra.co.in/transaction/orders/ to view the order. Thank You for ordering. Delivery of your book order will be attempted by CADABRA within one week.')

        send_sms(mobiles=instance.requester_address.phone_number, message='An exchange order has been created for "' + instance.requester_book.book_name +
                 '" from  user ' + instance.requester.username +
                 ' and "'+instance.offerrer_book.book_name +
                 '" from user ' + instance.offerrer.username +
                 '. Go to  https://www.cadabra.co.in/transaction/orders/ to view the order. Thank You for ordering. Delivery of your book order will be attempted by CADABRA within one week.')

# Done
@receiver(post_save, sender=Requests)
def send_request_email(sender, instance, created, **kwargs):

    if created:

        EmailThreadAPI(subject='New Request for book "'+instance.requester_book.book_name + '"',
                       text='You have recieved a new request from user "'+instance.requester.username + '" for book "' +
                       instance.requester_book.book_name +
                       '". Go to https://cadabra.co.in/transaction/offers/ for more details.', recepient=instance.offerrer.email).start()

# Done
@receiver(post_save, sender=FinalBuyOrder)
def send_buyorder_email(sender, instance, created, **kwargs):

    if created:

        EmailThreadAPI(subject='Buy Order successfully placed',
                       text='You have successfully ordered book "' + instance.book.book_name + '" . Amount payable is Rs ' +
                       str(instance.total_price) +
                       '. Go to  https://www.cadabra.co.in/transaction/orders/ to view the order. CADABRA will deliver the book within one week.',
                       recepient=instance.user.email).start()

        EmailThreadAPI(subject='Order for your book "' + instance.book.book_name + '"',
                       text='Your book "' +
                       instance.book.book_name + '" has been sold to user'+instance.user.username+
                       '. You can view the item at http://cadabra.co.in/userbooks/sold/. CADABRA will pick up the book within one week.',
                       recepient=instance.seller.email).start()

        send_sms(mobiles=instance.selleraddress.phone_number, message='Your book "' +
                 instance.book.book_name + '" has been sold. CADABRA will pick up the book within one week.')

# Done
@receiver(post_save, sender=CompletedTransaction)
def send_completed_transaction_email(sender, instance, created, **kwargs):

    if created:

        EmailThreadAPI(subject='Delivery Completed ',
                       text='Delivery for "' + instance.requester_book_name +
                       '" from "' + instance.requester.username +
                       '" and "'+instance.offerrer_book_name +
                       '" from "' + instance.offerrer.username +
                       '" has been completed. Thank You for using CADABRA.',
                       recepient=instance.offerrer.email).start()

        EmailThreadAPI(subject='Delivery Completed ',
                       text='Delivery for "' + instance.requester_book_name +
                       '" from "' + instance.requester.username +
                       '" and "'+instance.offerrer_book_name +
                       '" from "' + instance.offerrer.username +
                       '" has been completed. Thank You for using CADABRA.',
                       recepient=instance.requester.email).start()

#Done
@receiver(post_save, sender=CompletedBuyOrder)
def send_completed_buy_order_email(sender, instance, created, **kwargs):

    if created:

        EmailThreadAPI(subject='Delivery Completed ',
                       text='Delivery for "' + instance.book_name +
                       '" has been completed. Thank you for using CADABRA.',
                       recepient=instance.user.email).start()

# Done
@receiver(pre_delete, sender=Requests)
def cancel_requests_email(sender, instance, **kwargs):

        EmailThreadAPI(subject='Request cancelled for "' + instance.requester_book.book_name + '"',
                       text='Request for "' + instance.requester_book.book_name + '" from "' +
                       instance.requester.username +
                       '" is cancelled. Go to https://www.cadabra.co.in/ for more details.', recepient=instance.offerrer.email).start()

# Done
@receiver(pre_delete, sender=Transaction)
def delete_transaction_email(sender, instance, **kwargs):

        EmailThreadAPI(subject='Exchange Order cancelled ',
                       text='An exchange order has been cancelled for book "' + instance.requester_book.book_name +
                       '" from "' + instance.requester.username +
                       '" and book "'+instance.offerrer_book.book_name +
                       '" from "' + instance.offerrer.username +
                       '".Go to https://www.cadabra.co.in/ for more books. Thank You for using CADABRA.',
                       recepient=instance.offerrer.email).start()

        EmailThreadAPI(subject='Exchange Order cancelled ',
                       text='An exchange order has been cancelled for book "' + instance.requester_book.book_name +
                       '" from "' + instance.requester.username +
                       '" and book "'+instance.offerrer_book.book_name +
                       '" from "' + instance.offerrer.username +
                       '".Go to https://www.cadabra.co.in/ for more books. Thank You for using CADABRA.',
                       recepient=instance.requester.email).start()

        send_sms(mobiles=instance.offerrer_address.phone_number, message='An exchange order has been cancelled for book "' + instance.requester_book.book_name +
                       '" from ' + instance.requester.username +
                       ' and book '+instance.offerrer_book.book_name +
                       ' from "' + instance.offerrer.username +
                       '".')

# Done
@receiver(pre_delete, sender=FinalBuyOrder)
def delete_buyorder_email(sender, instance, **kwargs):

    EmailThreadAPI(subject='Buy Order cancelled',
                   text='Buy Order for book "' + instance.book.book_name + '" is cancelled from user.',
                   recepient=instance.seller.email).start()

    send_sms(mobiles=instance.selleraddress.phone_number, message='Buy Order for book "' +
             instance.book.book_name + '" is cancelled from user '+instance.user.username+'.')
