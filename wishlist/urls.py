from wishlist import views
from django.urls import path


urlpatterns = [
    path('list/<int:item_id>/add', views.add_to_list, name='add_to_list'),
    path('wishlist/', views.WishListView.as_view(), name='wish_list'),
    path('list/<int:item_id>/delete', views.delete_from_list, name='delete_item'),

]
