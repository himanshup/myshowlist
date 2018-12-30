from django.urls import path
from .views import UserDetail, LoginView, RegisterView, ListView, EntryDetail, LogoutView


urlpatterns = [
    path('users/<int:pk>/', UserDetail.as_view()),
    path('list/', ListView.as_view()),
    path('list/<int:pk>/<str:status>/<str:sort>/<str:direction>/', ListView.as_view()),
    path('entry/<int:pk>/', EntryDetail.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/register/', RegisterView.as_view())
]
