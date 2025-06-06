from django.urls import path
from users.views import UserListCreateView, UserRetrieveUpdateDestroyView, CurrentUserView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]