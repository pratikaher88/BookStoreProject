from wishlist import views
from django.urls import path

app_name='wishlist'

urlpatterns = [
    path('<int:item_id>/add', views.add_to_list, name='add_to_list'),
    path('wishlist/', views.wish_list_entries_view, name='wish_list'),
    path('wishlist/finalorder/',
         views.FinalBuyOrderListView.as_view(), name='final_order'),
    path('<int:item_id>/delete', views.delete_from_list, name='delete_item'),
    path('wishlist/<int:pk>/delete',
         views.FinalBuyOrderDeleteView.as_view(), name='finalorder-delete'),
    

]
