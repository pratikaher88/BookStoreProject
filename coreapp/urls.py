from django.conf.urls import url
from coreapp import views
from django.urls import path

app_name='coreapp'

urlpatterns = [
    
    path('', views.BookListView.as_view(), name='list_entries'),
    path('buy/', views.BuyListView.as_view(), name='buy_entries'),
    path('exchange/', views.ExchangeListView.as_view(), name='exchange_entries'),
    path('newentry/',views.NewEntry.as_view(),name='new_entry'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit',views.update_profile,name='profile_edit'),
    path('profile/address/edit', views.update_address,name='address_edit'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('userbooks/', views.UserBookListView.as_view(),name='userbooks'),
    path('userbooks/<str:username>', views.UserBookListViewForUser.as_view(),name='userbooksforuser'),
    path('userbooks/<int:pk>/update',views.PostUpdateView.as_view(),name='post-update'),
    path('userbooks/<int:pk>/delete',views.PostDeleteView.as_view(),name='post-delete'),
]
