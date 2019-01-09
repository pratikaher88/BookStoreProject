from django.conf.urls import url
from transaction import views
from django.urls import path

app_name = 'transaction'

urlpatterns = [

    path('<int:book_id>/add', views.add_request, name='add_request'),
    path('requests/', views.RequestListView.as_view(), name='requests_view'),
    path('requests/<int:pk>/delete',views.RequestDeleteView.as_view(), name='request-delete'),
    path('offers/', views.OfferListView.as_view(), name='offers_view'),
    path('orders/', views.TransactionListView.as_view(), name='orders_view'),
    path('orders/<int:pk>/delete', views.TransactionDeleteView.as_view(),name='order-delete'),

]
