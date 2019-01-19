from cart import views
from django.urls import path

app_name='cart'

urlpatterns = [
    path('<int:item_id>/add', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_list_entries_view, name='cart_items'),
    path('<int:item_id>/delete', views.delete_from_cart, name='delete_item'),
    path('cart/<int:pk>/delete',
         views.FinalBuyOrderDeleteView.as_view(), name='finalorder-delete'),
    

]
