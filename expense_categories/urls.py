from django.urls import path
from .views import ExpenseCategoryListCreateView, ExpenseCategoryRetrieveUpdateDestroyView

urlpatterns = [
    path('', ExpenseCategoryListCreateView.as_view(), name='expense-category-list-create'),
    path('<int:pk>/', ExpenseCategoryRetrieveUpdateDestroyView.as_view(), name='expense-category-retrieve-update-destroy'),
]