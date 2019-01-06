from django.conf.urls import url
from transaction import views
from django.urls import path

app_name = 'transaction'

urlpatterns = [

    path('requests/', views.requestsview, name='requests_view'),
    # path('offers/', views.BookListView.as_view(), name='list_entries'),
    # path('orders/', views.BookListView.as_view(), name='list_entries'),

]
