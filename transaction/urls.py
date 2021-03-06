from django.conf.urls import url
from transaction import views
from django.urls import path

app_name = 'transaction'

urlpatterns = [

    path('<int:book_id>/add', views.add_request, name='add_request'),
    path('requests/', views.RequestListView.as_view(), name='requests_view'),
    path('requests/<int:pk>/delete',views.RequestDeleteView.as_view(), name='request-delete'),
    path('offers/', views.OfferListView.as_view(), name='offers_view'),
    path('offers/<int:pk>/delete', views.OfferDeleteView.as_view(), name='offer-delete'),
    path('offers/<int:offer_id>/<int:book_id>/finaltransaction', views.final_transaction ,name='final-transaction'),
    path('orders/', views.TransactionListView.as_view(), name='orders_view'),
    path('orders/<int:pk>/delete', views.TransactionDeleteView.as_view(),name='order-delete'),
    path('orders/exchange-orders',
         views.TransactionCompletedExchangeOrder.as_view(), name='exchange-order'),
    path('orders/buy-orders', views.TransactionCompletedBuyOrder.as_view(), name='buy-order'),

]
