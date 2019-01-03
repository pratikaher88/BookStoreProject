from django.urls import path
from search import views

app_name = 'searchapp'

urlpatterns = [
    path('', views.SearchListView.as_view(), name='search'),
    path('content-autocomplete/', views.ContentAutoComplete.as_view(),name='content-autocomplete'),
    path('search1/', views.SearchAutoComplete.as_view(), name='search1'),
]
