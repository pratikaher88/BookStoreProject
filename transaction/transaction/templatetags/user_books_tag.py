from django import template
from coreapp.models import Profile
from django.shortcuts import get_object_or_404
register = template.Library()


@register.filter
def user_books_for_user(collection_all, user_username):
    print(user_username)
    user_profile = get_object_or_404(Profile, user__username=user_username)
    collection_items = collection_all.get(
        owner=user_profile)
    
    return collection_items.books.filter(
        sell_or_exchange='Exchange')
