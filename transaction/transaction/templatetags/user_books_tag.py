from django import template
from coreapp.models import Profile, Transaction, FinalBuyOrder
from django.shortcuts import get_object_or_404
register = template.Library()


@register.filter
def user_books_for_user(collection_all, user_username):
    ordered_books = FinalBuyOrder.objects.values_list('book')
    requester_books = Transaction.objects.values_list('requester_book')
    offerrer_books = Transaction.objects.values_list('offerrer_book')
    
    user_profile = get_object_or_404(Profile, user__username=user_username)
    collection_items = collection_all.get(
        owner=user_profile)
    
    return collection_items.books.filter(
        sell_or_exchange='Exchange').exclude(id__in=ordered_books).exclude(id__in=offerrer_books).exclude(id__in=requester_books)

@register.filter
def author_list(authors):

    if authors:
        author_name = ",".join(authors)

        return author_name + '.'
    else:
        return authors

