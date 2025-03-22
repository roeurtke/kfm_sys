from django.urls import path
from .views import ExpanseListCreateView, ExpanseRetrieveUpdateDestroyView

urlpatterns = [
    path('', ExpanseListCreateView.as_view(), name='expanse-list-create'),
    path('<int:pk>/', ExpanseRetrieveUpdateDestroyView.as_view(), name='expanse-retrieve-update-destroy'),
]