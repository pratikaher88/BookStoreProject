from django.conf.urls import url
from coreapp import views
from django.urls import path


urlpatterns = [
    
    path('',views.BookListView.as_view(),name='listentries'),
    path('newentry/',views.NewEntry.as_view(),name='newentry'),
    path('profile/',views.profile,name='profile'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    # path('addforexchange/',views.addforexchange(),name='addforexchange')
    # path('exchangelist/',views.addforexchange(),name='addforexchange')
    # path('logoutpage/', views.logoutpage , name='logoutpage'),
    # path('transactions/',views.TransactionListView(),name='tansactions'),
    path('userbooks/', views.UserBookListView.as_view(),name='userbooks'),
    path('userbooks/<str:username>', views.UserBookListViewForUser.as_view(),name='userbooksforuser'),
    path('userbooks/<int:pk>/update',views.PostUpdateView.as_view(),name='post-update'),
    path('userbooks/<int:pk>/delete',views.PostDeleteView.as_view(),name='post-delete'),
]