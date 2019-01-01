from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CONITION_CHOICES = (
    ('Acceptable','Acceptable'),
    ('Bad', 'Bad'),
    ('Good','Good'),
)

class Book(models.Model):

    user = models.ForeignKey(User ,on_delete = models.CASCADE ,null=True )
    book_name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image = models.ImageField(null=True, blank=True, upload_to="book_images/")
    price = models.IntegerField()
    condition = models.CharField(max_length=100,choices = CONITION_CHOICES, default='Acceptable')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.book_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='avatar.jpg', upload_to="profile_images/")
    # Books = models.ManyToManyField(Book)


    def __str__(self):
        return self.user.username

# class Cart(models.Model):
#     user = models.ForeignKey(User ,on_delete = models.CASCADE ,null=True)
#     book = modes.ForeignKey(Book)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=Book)
# def create_user_list(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# class UserBooks(models.Model):
    
#     user = models.ForeignKey(User ,on_delete = models.CASCADE ,null=True)
#     book = models.ManyToManyField( Book )

#     def __str__(self):
#         return self.book_name