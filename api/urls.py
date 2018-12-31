from django.urls import path
from .views import UserDetail, LoginView, RegisterView, LogoutView, ListView, EntryDetail, ShowsView, ShowDetail


urlpatterns = [
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/list/', ListView.as_view()),
    path('users/<int:userId>/entry/<int:pk>/', EntryDetail.as_view()),
    path('shows/', ShowsView.as_view()),
    path('shows/<int:pk>/', ShowDetail.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/register/', RegisterView.as_view())
]
